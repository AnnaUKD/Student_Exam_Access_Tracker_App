import os
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentInfoForm, GroupJournalForm
# from .services.student_service import get_student_info
from .services.student_service import get_student_info, student_app_functional
from django.urls import reverse
from core.models import GroupJournal
# Create your views here.



def student_view(request):
    context = {
        "title": "Student Exam Access Status Tracker",
        "message": "Ви зараз знаходитися в моєму веб-додатку, який створений для відстеження статусу допуску до екзамену.",
    }
    return render(request=request, template_name='student_exam_access_tracker/index.html', context=context)


def result_view(request):
    student = student_app_functional(request.session.get('student_form_data'))
    context = {
        # "full_name": request.session.get('full_name', 'я не працюю'),
        "title": "Student Exam Access Result",
        "message1": "Ось результат Вашого обрахунку.",
        "message2": "Бажаю Вам успішно закінчити твій семестр.",
        "student": student,
    }
    del request.session['student_form_data']
    return render(request=request, template_name='student_exam_access_tracker/result.html', context=context)


def check_student_view(request):
    if request.method == "POST":
        form = StudentInfoForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            student_form_data = form.cleaned_data
            request.session["student_form_data"] = student_form_data
            return redirect(reverse('result'))
    else:
        form = StudentInfoForm()

    context = {
        "form": form,
    }
    return render(request=request, template_name='student_exam_access_tracker/form.html', context=context)


def get_group_journals_view(request):
    group_journals = GroupJournal.objects.all()
    context = {
        'title': 'List of group journals',
        'data': group_journals,
    }
    return render(request=request, template_name='student_exam_access_tracker/group_journals_list.html', context=context)


def get_group_journal_view(request, pk: int):
    group_journal = get_object_or_404(klass=GroupJournal, pk=pk)
    context = {
        'title': 'Details about journal',
        'data': group_journal,
    }
    return render(request=request, template_name='student_exam_access_tracker/group_journal_details.html', context=context)


def create_group_journal_view(request):
    if request.method == "POST":
        form = GroupJournalForm(request.POST)
        if form.is_valid():
            group_journal = form.save()
            return redirect('group_journal_detail', pk=group_journal.pk)
    else:
        form = GroupJournalForm()
    context = {
        'title': 'Create new journal',
        'form': form,
    }
    return render(request=request, template_name='student_exam_access_tracker/group_journal_form.html', context=context)


def update_group_journal_view(request, pk: int):
    group_journal = get_object_or_404(klass=GroupJournal, pk=pk)
    if request.method == "POST":
        form = GroupJournalForm(request.POST, instance=group_journal)
        if form.is_valid():
            group_journal = form.save()
            return redirect('group_journal_detail', pk=group_journal.pk)
    else:
        form = GroupJournalForm(instance=group_journal)
    context = {
        'title': 'Update journal',
        'form': form,
    }
    return render(request=request, template_name='student_exam_access_tracker/group_journal_form.html', context=context)