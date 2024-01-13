from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from .views import StaffList, StaffLogin, StaffRegistration, StudentLogin, SubjectRegistration, TeacherLogin, TeacherRegistration, StudentRegistration, StudentList, TeacherList, LevelRegistration, LevelSectionRegistration, StaffPositionRegistration, UserLogOut, load_level_section

app_name = 'account'

urlpatterns = [
    path('student-registration/', StudentRegistration.as_view(), name='student-registration'),
    path('teacher-registration/', TeacherRegistration.as_view(), name='teacher-registration'),
    path('staff-registration/', StaffRegistration.as_view(), name='staff-registration'),
    path('student-list/', StudentList.as_view(), name='student-list'),
    path('teacher-list/', TeacherList.as_view(), name='teacher-list'),
    path('staff-list/', StaffList.as_view(), name='staff-list'),
    path('subject-registration/', SubjectRegistration.as_view(), name='subject-registration'),
    path('student-login/', StudentLogin.as_view(), name='student-login'),
    path('teacher-login/', TeacherLogin.as_view(), name='teacher-login'),
    path('staff-login/', StaffLogin.as_view(), name='staff-login'),
    # path('after-teacher-login/', AfterTeacherLogin.as_view(), name='after-teacher-login'),
    path('level-registration/', LevelRegistration.as_view(), name='level-registration'),
    path('level-section-registration/', LevelSectionRegistration.as_view(), name='level-section-registration'),
    path('staff-position-registration/', StaffPositionRegistration.as_view(), name='staff-position-registration'),
    path('user_logout/', UserLogOut.as_view(), name='user_logout'),
  

    # url('^', include('django.contrib.auth.urls')),

    path('load-section/', load_level_section, name='load-section'),
    # path('multiple-subjects/', multiple_subjects, name='multiple-subjects'),

    # path('load-subject/', load_level_subject, name='load-subject'),
]