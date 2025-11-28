# def get_student_info(student: dict):
#     if student.get('first_name') == 'Анна':
#         print('Допущена до сесії')
#     else:
#         print('Не допущено до сесії')

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from StudentExamAccessTrackerApp.settings import BASE_DIR

SPREADSHEET_ID = "10NO-Hv4qoTwgYA9d8sVAUwboMf_zZUba-LBcS3a451U"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

GRADEBOOKS = {
    "ІПЗс-24-1": "1rulJUfgXuEVv4SP6olUYSAEWWd1pWTmWAAxkXeJ5DN0",
    "ІПЗс-24-2": "10NO-Hv4qoTwgYA9d8sVAUwboMf_zZUba-LBcS3a451U",
    "ІПЗс-24-3": "1HIQlFrzo30aJNJUcydgt4xWBTSmOmSVeOF0wK-u274o",
}

PAGES = [
    "Цінності громадянського суспільства",
    "Алгоритми та структури даних",
    "Інженерія програмного забезпечення",
    "Комп`ютерна дискретна математика",
    "Людино-машинна взаємодія",
    "Іноземна мова (за професійним спрямуванням)",
    "Підсумок",
]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)


def get_credentials():
    creds = None
    token_path = BASE_DIR / "core" / "services" / "token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # if os.path.exists("credentials.json"):
            #     print('exists')
            credential_path = BASE_DIR / "core" / "services" / "credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            # flow = InstalledAppFlow.from_client_secrets_file("C:\\Users\\Anna\\PycharmProjects\\StudentExamAccessTrackerApp\\core\\services\\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds


def build_service(creds):
    return build("sheets", "v4", credentials=creds)


def call_api(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get("values", [])
    if not values:
        print("No data found.")
        return []
    return values


def get_student_names(service, sheet_name, group_id):
    values = call_api(service, spreadsheet_id=group_id, range_name=f"{sheet_name}!B5:B")
    return [row[0] if len(row) > 0 else None for row in values]


def get_grades_table(service, sheet_name, group_id):
    values = call_api(service, spreadsheet_id=group_id, range_name=f"{sheet_name}!F5:CL")
    return pd.DataFrame(values)


def get_average_grades_sixty(service, sheet_name, group_id):
    values = call_api(service, spreadsheet_id=group_id, range_name=f"{sheet_name}!CQ5:CQ")
    return [row[0] if len(row) > 0 else None for row in values]


def get_average_grades_five(service, sheet_name, group_id):
    values = call_api(service, spreadsheet_id=group_id, range_name=f"{sheet_name}!CP5:CP")
    return [row[0] if len(row) > 0 else None for row in values]


def build_students_dataframe(names, grades):
    df = pd.DataFrame({"Student Name": names})
    grades_df = pd.DataFrame(grades)
    grades_df.insert(0, "Student Name", df["Student Name"].values)
    return grades_df


def build_average_dataframe(names, averages):
    if len(averages) < len(names):
        averages += [None] * (len(names) - len(averages))
    else:
        averages = averages[:len(names)]
    df_average_grade = pd.DataFrame({
        "Student Name": names,
        "Average grade_in_sixty_score_system": averages
    })
    return df_average_grade


def merge_grades_with_averages(grades_df, avg_sixty_df, avg_five_list):
    grades_df = grades_df.reset_index(drop=True)
    merged = grades_df.merge(avg_sixty_df, on="Student Name", how="left")
    if len(avg_five_list) < len(merged):
        avg_five_list += [None] * (len(merged) - len(avg_five_list))
    else:
        avg_five_list = avg_five_list[:len(merged)]
    merged["Average grade_in_five_score_system"] = avg_five_list
    merged["Average grade_in_sixty_score_system"] = pd.to_numeric(
        merged["Average grade_in_sixty_score_system"], errors="coerce"
    )
    return merged


def assign_status(df):
    df["Статус"] = df["Average grade_in_sixty_score_system"].apply(
        lambda x: "Допущено до сесії" if pd.notna(x) and x >= 35 else "Не допущено до сесії"
    )
    return df


def search_student(df, name_input):
    mask = df["Student Name"].str.contains(name_input, case=False, na=False)
    result = df[mask]
    if result.empty:
        print("Студента не знайдено. Перевірте правильність написання.")
    else:
        print("\nЗнайдено студента(-ів):")
        print(result[["Student Name", "Average grade_in_five_score_system", "Average grade_in_sixty_score_system",
                      "Статус"]])


def student_search(df):
    while True:
        user_input = input("Введіть ПІБ студента (повністю або частково) або 'exit' для виходу: ")
        if user_input.lower() == "exit":
            print("Вихід з пошуку студентів.")
            break
        search_student(df, user_input)


def row_to_dict(row):
    return {col: row[col] for col in row.index}


def df_to_dict_list(df):
    return [row_to_dict(row) for _, row in df.iterrows()]


def search_student_dict(df, name_input):
    mask = df["Student Name"].str.contains(name_input, case=False, na=False)
    results = df[mask]

    if results.empty:
        return []

    return df_to_dict_list(results)


def get_student_info(student: dict):
    first_name = student.get("first_name", "None").strip()
    last_name = student.get("last_name", "None").strip()
    middle_name = student.get("middle_name", "None").strip()
    full_name = f"{last_name} {first_name} {middle_name}".strip()

    return full_name


def student_app_functional(student: dict):
    try:
        creds = get_credentials()
        service = build_service(creds)

        last_name = student.get("last_name")
        first_name = student.get("first_name")
        middle_name = student.get("middle_name")

        full_name = f'{last_name} {first_name} {middle_name}'

        group_id = GRADEBOOKS.get(student.get("group_code"))

        names_list = get_student_names(service, student.get("discipline_name"), group_id)
        grades_values = get_grades_table(service, student.get("discipline_name"), group_id)
        avg_sixty_list = get_average_grades_sixty(service, student.get("discipline_name"), group_id)
        avg_five_list = get_average_grades_five(service, student.get("discipline_name"), group_id)

        grades_df = build_students_dataframe(names_list, grades_values)
        avg_sixty_df = build_average_dataframe(names_list, avg_sixty_list)
        merged_df = merge_grades_with_averages(grades_df, avg_sixty_df, avg_five_list)
        final_df = assign_status(merged_df)

        mask = final_df["Student Name"].str.fullmatch(full_name, case=False, na=False)
        student_row = final_df[mask]

        if student_row.empty:
            return {
                "error": "Студента не знайдено. Перевірте правильність ПІБ."
            }

        student_row = student_row.iloc[0]

        if 'Підсумок' in PAGES:
            PAGES.remove('Підсумок')

        student_dict = {
            "surname": last_name,
            "name": first_name,
            "middle_name": middle_name,
            "course": student.get("discipline_name"),
            "group_code": student.get("group_code"),
            "average_five": student_row["Average grade_in_five_score_system"],
            "average_sixty": student_row["Average grade_in_sixty_score_system"],
            "status": student_row["Статус"],
        }

        return student_dict

    except HttpError as err:
        return {"error": str(err)}
