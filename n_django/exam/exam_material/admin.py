from django.contrib import admin
from .models import  Quiz, Question, Answer, Result

# @admin.register(Category)
# class CatAdmin(admin.ModelAdmin):
# 	list_display = [
#         'name',
#         ]   
        
# @admin.register(Quiz)
# class QuizAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 
#         'title',
#         'subject',
#         'difficulty',
#     ]  
    
#     #allows to add answer while creating the question itself
#     inlines = [QuestionInLine, AnswerInLineModel,] 
    

class QuestionInLineModel(admin.TabularInline):
    model = Question
    fields = [
          'title',
    ]

class AnswerInLineModel(admin.TabularInline):
    model = Answer
    fields = [
        'question',
        'answer_text', 
        'correct'
        ]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'exam_name',
        ]
    list_display = [
        'title', 
        'exam_name',
        'date_updated',
        ]
    
    #allows to add answer while creating the question itself
    inlines = [AnswerInLineModel,] 

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'question',
        'answer_text', 
        'correct', 
        ]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title',
        'subject',
    ]  
    
    #allows to add answer while creating the question itself
    inlines = [QuestionInLineModel,] 

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'exam_name',
        'score',
    ]