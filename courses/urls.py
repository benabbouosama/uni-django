from django.urls import path
from django.urls import path
from . import views
from django.urls import re_path
from django.views.static import serve
from app import settings
urlpatterns = [
    path('<int:pk>/create_course/', views.create_course, name='create_course'),
    path('search_courses/', views.display_pdf, name='search_courses'),
   # path('save_calendar_pdf/', views.save_calendar_pdf, name='save_calendar_pdf'),
    path('save_schedule/', views.save_schedule, name='save_schedule'),
    path('internal/choose-level-submit/', views.choose_level_submit, name='choose_level_submit'),
    path('Schedules', views.create_schedule, name='create_schedule'),
    path('download/<int:course_id>/', views.download_pdf_file, name='download_pdf_file'),
    path('schedules/<str:level>/', views.display_schedule, name='display_schedule'),
    path('select_level/', views.select_level, name='select_level'),
    path('delete_module/<int:module_id>/', views.delete_module, name='delete_module'),
    path('download_news_pdf/<int:news_id>/', views.download_news_pdf, name='download_news_pdf'),


]