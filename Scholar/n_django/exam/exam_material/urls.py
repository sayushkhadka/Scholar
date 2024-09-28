from django.urls import path, include
from .views import QuizListView, quiz_view, quiz_data_view, save_quiz_view, QuestionList, QuestionCreate, QuestionUpdate, delete_answer, ExamRegistrationStaff, ExamRegistrationTeacher, ResultListStaff, ResultListTeacher, ExamList,  questionAnswer, ExamDelete, ExamDetail, ExamUpdate, QuestionDelete, QuestionDetail

app_name = 'exam_material'

urlpatterns = [
    # path('quiz-api/', QuizAPI.as_view(), name='quiz-api'),
    # # path('r/<str:topic>/', RandomQuestion.as_view(), name='random' ),
    # path('question/<str:topic>/', QuizQuestion.as_view(), name='question-api'),
    # path('answer/<str:topic>/', QuizAnswer.as_view(), name='answer-api'),

    path('quiz-main/', QuizListView.as_view(), name='quiz-main'),
    path('quiz-main/<pk>', quiz_view, name='quiz-view'),
    path('quiz-main/<pk>/save/', save_quiz_view, name='save-quiz-view'),
    path('quiz-main/<pk>/data/', quiz_data_view, name='quiz-data-view'),

    path('question-create/', QuestionCreate.as_view(), name='question-create'),
    path('question-list/', QuestionList.as_view(), name='question-list'),
    path('question-detail/<int:pk>/', QuestionDetail.as_view(), name ='question-detail'),
    path('question-update/<int:pk>/', QuestionUpdate.as_view(), name='question-update'),
    path('question-delete/<int:pk>/', QuestionDelete.as_view(), name='question-delete'),

    path('answer-delete/<int:pk>/', delete_answer, name='answer-delete'),

    path('exam-registration-staff/', ExamRegistrationStaff.as_view(), name='exam-registration-staff'),
    path('exam-registration-teacher/', ExamRegistrationTeacher.as_view(), name='exam-registration-teacher'),
    path('exam-list/', ExamList.as_view(), name='exam-list'),
    path('exam-detail/<int:pk>/', ExamDetail.as_view(), name='exam-detail'),
    path('exam-update/<int:pk>/', ExamUpdate.as_view(), name ='exam-update'),
    path('exam-delete/<int:pk>/', ExamDelete.as_view(), name='exam-delete'),

    path('question-answer/', questionAnswer, name='question-answer'),

    path('exam-result-list-teacher/', ResultListTeacher.as_view(), name='exam-result-list-teacher'),
    path('exam-result-list-staff/', ResultListStaff.as_view(), name='exam-result-list-staff'),
] 