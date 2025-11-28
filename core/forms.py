from django import forms

class StudentInfoForm(forms.Form):
    last_name = forms.CharField(label="Прізвище", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(max_length=100, label="По батькові", widget=forms.TextInput(attrs={'class': 'form-control'}))
    group_code = forms.CharField(max_length=100, label="Шифр групи", widget=forms.TextInput(attrs={'class': 'form-control'}))
    discipline_name = forms.CharField(max_length=100, label="Дисципліна, з якої Ви хочете дізнатися успішність", widget=forms.TextInput(attrs={'class': 'form-control'}))