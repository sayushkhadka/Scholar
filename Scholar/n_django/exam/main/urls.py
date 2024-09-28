from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Index, StudentPage, TeacherPage, StaffPage, staffNoticeBoard, commentNotice, staffCreateNotice, studentNoticeBoard, staffNoticeView, teacherNoticeBoard, teacherCreateNotice, teacherNoticeView, StudentList, StudentDetail, StudentUpdate, StudentDelete, TeacherList, TeacherDetail, TeacherUpdate, TeacherDelete, StaffList, StaffDetail, StaffUpdate, StaffDelete

app_name = 'main'

urlpatterns = [
    #pages
    path('', Index.as_view(), name='index'),
    path('student-page/', StudentPage.as_view(), name='student-page'),
    path('teacher-page/', TeacherPage.as_view(), name='teacher-page'),
    path('staff-page/', StaffPage.as_view(), name='staff-page'),

    # Notice Board
    path('staff-notice-board/',staffNoticeBoard,name='staff-notice-board'),
    path('student-notice-board/',studentNoticeBoard,name='student-notice-board'),
    path('staff-notice-view/',staffNoticeView,name='staff-notice-view'),
    path('teacher-notice-view/',teacherNoticeView,name='teacher-notice-view'),
    path('staff-create-notice/',staffCreateNotice,name='staff-create-notice'),
    path('teacher-create-notice/',teacherCreateNotice,name='teacher-create-notice'),
    path('comment-notcie/',commentNotice,name='comment-notice'),
    path('teacher-notice-board/',teacherNoticeBoard,name='teacher-notice-board'),

    #Student account crud
    path('student-list/', StudentList.as_view(), name='student-list'),
    path('student-detail/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('student-update/<int:pk>/', StudentUpdate.as_view(), name ='student-update'),
    path('studnet-delete/<int:pk>/', StudentDelete.as_view(), name='student-delete'),

    #Teacher account crud
    path('teacher-list/', TeacherList.as_view(), name='teacher-list'),
    path('teacher-detail/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
    path('teacher-update/<int:pk>/', TeacherUpdate.as_view(), name ='teacher-update'),
    path('teacher-delete/<int:pk>/', TeacherDelete.as_view(), name='teacher-delete'),

    #Staff account crud
    path('staff-list/', StaffList.as_view(), name='staff-list'),
    path('staff-detail/<int:pk>/', StaffDetail.as_view(), name='staff-detail'),
    path('staff-update/<int:pk>/', StaffUpdate.as_view(), name ='staff-update'),
    path('staff-delete/<int:pk>/', StaffDelete.as_view(), name='staff-delete'),


    #path('after-teacher-login/', AfterTeacherLogin.as_view(), name='after-teacher-login'),
]