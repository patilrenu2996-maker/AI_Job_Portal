from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.jobs, name='jobs'),
    path('search/', views.search_jobs, name='search_jobs'),
    path('profile/', views.profile, name='profile'),
    path('improve-resume/', views.improve_resume, name='improve_resume'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('generated-resume/',views.generated_resume,name='generated_resume'),
    path('download-improved-resume/',views.download_improved_resume,name='download_improved_resume'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('save-job/<int:job_id>/', views.save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs')
    ]