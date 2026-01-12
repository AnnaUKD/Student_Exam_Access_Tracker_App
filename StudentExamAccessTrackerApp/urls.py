"""
URL configuration for StudentExamAccessTrackerApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.student_view, name='index'),
    path('result/', views.result_view, name='result'),
    path('student_form/', views.check_student_view, name='student_form'),
    path('group_journals/', views.get_group_journals_view, name='group_journals_list'),
    path('group_journal/<int:pk>/', views.get_group_journal_view, name='group_journal_detail'),
    path('group_journal/create/', views.create_group_journal_view, name='group_journal_create'),
    path('group_journal/update/<int:pk>/', views.update_group_journal_view, name='group_journal_update'),
]
