from rest_framework import serializers
from .models import Quiz, Question, Answer


#like form in general sense
class QuizSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        # fields = [
        #     'title',
        # ]
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        # fields = [
        #     'id',
        #     'answer_text',
        #     'correct',
        # ]
        fields = '__all__'

# class RandomQuestionSerializer(serializers.ModelSerializer):

#     answer = AnswerSerializer(many=True, read_only=True)

#     class Meta:
    
#         model = Question
#         fields = [
#             'title','answer',
#         ]

class QuestionSerializer(serializers.ModelSerializer):


    answer = AnswerSerializer(many=True, read_only=True) #gets everything from AnswerSerializer class(is, answer_text, correct)
    exam_name = QuizSerializer(read_only=True) #gets everything from QuizSerializer class(title)

    class Meta:
    
        model = Question
        # fields = [
        #     'exam_name','title','answer', #this 'title' is the question title
        # ]
        fields = '__all__'