from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory

from .forms import QuestionForm, AnswerForm, AnswerFormSet, ExamRegistrationForm

# from rest_framework.response import Response
# from rest_framework import generics
from .models import Quiz, Question, Answer, Result
# from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer
# from rest_framework.views import APIView


from django.http import JsonResponse

# class QuizAPI(generics.ListAPIView):
#     serializer_class = QuizSerializer
#     queryset = Quiz.objects.all()

# # class RandomQuestion(APIView):

# #     def get(self, request, format=None, **kwargs):
# #         question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
# #         serializer = RandomQuestionSerializer(question, many=True)
# #         return Response(serializer.data)

# class QuizQuestion(APIView):

#     def get(self, request, format=None, **kwargs):
#         quiz = Question.objects.filter(quiz__title=kwargs['topic'])
#         serializer = QuestionSerializer(quiz, many=True)
#         return Response(serializer.data)


# class QuizAnswer(APIView):

#     def get(self, request, format=None, **kwargs):
#         answer = Answer.objects.filter(answer__title=kwargs['topic'])
#         serializer = AnswerSerializer(answer, many=True)
#         return Response(serializer.data)


class QuizListView(generic.ListView):
    model = Quiz
    template_name = 'exam_material/quiz_main.html'

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'exam_material/quiz.html', {'obj': quiz})

def quiz_data_view(request, pk):
        
    quiz = Quiz.objects.get(pk=pk)
    questions = []

    for q in quiz.get_questions():
        answers = []

        for a in q.get_answers():
            answers.append(a.answer_text)

        questions.append({str(q): answers}) #dict where q is question as the key and assigning it with its respective list of answers

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def save_quiz_view(request, pk):

    # print(request.POST)
    if request.is_ajax():
        questions = [] 
        data = request.POST
        data_= dict(data.lists()) #transforms QueryDict to ordinary Dict
        # print(type(data))
        # print(type(data_))
        # print((data_))
        
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            # print('key: ', k)
            question = Question.objects.get(title=k)
            questions.append(question)
        # print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100/ quiz.numberOfQuestions
        results = []
        correct_answer = None

        for q in questions:
            answer_selected = request.POST.get(q.title)

            if answer_selected != '':
                question_answers = Answer.objects.filter(question=q)

                for a in question_answers:
                    if answer_selected == a.answer_text:
                        if a.correct:
                            score +=1
                            correct_answer = a.answer_text
                            # print(correct_answer)
                    
                    else:
                        if a.correct:
                            correct_answer = a.answer_text
                            # print(correct_answer)

                results.append({str(q): {'correct_answer': correct_answer, 'answered': answer_selected}})

            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(exam_name=quiz, user=user, score=score_)
        

        if score_ >= quiz.scoreToPass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})

        else:
    
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

#Exam registration
class ExamRegistrationStaff(generic.CreateView):
    template_name = 'exam_material/exam_registration_form_staff.html'
    form_class = ExamRegistrationForm
    model = Quiz
    success_url = reverse_lazy('exam_material:exam-registration-staff')

    def form_valid(self, form) -> HttpResponse:
        # print(form.cleaned_data)
        self.object = form.save(commit=False)
        level_section = form.cleaned_data['levelSection']
        self.object.exam_section = level_section
        subject = self.object.subject
        title = self.object.title
        self.object.save()
        
        # print(level_section)
        messages.success(self.request, f"Exam name: '{title}' was registered successfully. Subject: '{subject}'")

        return super().form_valid(form)
    
class ExamRegistrationTeacher(generic.CreateView):
    template_name = 'exam_material/exam_registration_form_teacher.html'
    form_class = ExamRegistrationForm
    model = Quiz
    success_url = reverse_lazy('exam_material:exam-registration-teacher')

    def form_valid(self, form) -> HttpResponse:
        # print(form.cleaned_data)
        self.object = form.save(commit=False)
        level_section = form.cleaned_data['levelSection']
        self.object.exam_section = level_section
        subject = self.object.subject
        title = self.object.title
        self.object.save()
        
        # print(level_section)
        messages.success(self.request, f"Exam name: '{title}' was registered successfully. Subject: '{subject}'")

        return super().form_valid(form)
    
def questionAnswer(request):
    QuestionAnswerFormSet = modelformset_factory(Question, fields=('exam_name','title'), extra=4)

    if request.method == 'POST':
        form = QuestionAnswerFormSet(request.POST)
        # instances = form.save(commit=False)

        # for instance in instances:
        #     instance.save()

        instances = form.save()

    form = QuestionAnswerFormSet(queryset=Question.objects.none())
    return render(request, 'exam_material/questionAnswer.html', {'form': form})


class QuestionInline():
    form_class = QuestionForm
    model = Question
    template_name = 'exam_material/question_create_or_update.html'
    

    # def questionAnswer(request):
    #     QuestionAnswerFormSet = modelformset_factory(Question, fields=('exam_name','title'), extra=4)

        # if request.method == 'POST':
        #     form = QuestionAnswerFormSet(request.POST)
        #     # instances = form.save(commit=False)

        #     # for instance in instances:
        #     #     instance.save()

        #     instances = form.save()

        # form = QuestionAnswerFormSet(queryset=Question.objects.none())
        # return render(request, 'exam_material/questionAnswer.html', {'form': form})

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('exam_material:question-create')

    def formset_answers_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        answers = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for answer in answers:
            answer.question = self.object
            answer.save()


class QuestionCreate(QuestionInline, generic.CreateView):

    success_url = reverse_lazy('exam_material:question-create')

    def get_context_data(self, **kwargs):
        ctx = super(QuestionCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'answers': AnswerFormSet(prefix='answers'),
            }
        else:
            return {
                'answers': AnswerFormSet(self.request.POST or None, self.request.FILES or None, prefix='answers'),
            }


class QuestionUpdate(QuestionInline, generic.UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(QuestionUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'answers': AnswerFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='answers'),
        }
    
class QuestionList(generic.ListView):
    model = Question
    template_name = "exam_material/question-list.html"
    context_object_name = "questions"

def delete_answer(request, pk):
    try:
        answer = Answer.objects.get(id=pk)
    except Answer.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('exam_material:question-update', pk=answer.question.id)

    answer.delete()
    messages.success(
            request, 'Answer deleted successfully'
            )
    return redirect('exam_material:quiz-question-update', pk=answer.question.id)

class QuestionDetail(generic.DetailView):
    template_name = 'exam_material/question_detail.html'
    model= Question
    context_object_name = 'question_detail'
    queryset = Question.objects.all()

class QuestionDelete(generic.DeleteView):
    model = Question
    context_object_name = 'question_delete'
    success_url = reverse_lazy('exam_material:question-list')


class ResultListStaff(generic.ListView):
    template_name = 'exam_material/exam_result_list_staff.html'
    model = Result
    context_object_name = 'result_list_staff'
    queryset = Result.objects.all()

class ResultListTeacher(generic.ListView):
    template_name = 'exam_material/exam_result_list_teacher.html'
    model = Result
    context_object_name = 'result_list_teacher'
    queryset = Result.objects.all()


class ExamList(generic.ListView):
    template_name = 'exam_material/exam_list.html'
    model = Quiz
    context_object_name = 'exam_list'
    queryset = Quiz.objects.all()
    

class ExamDetail(generic.DetailView):
    template_name = 'exam_material/exam_detail.html'
    model= Quiz
    context_object_name = 'exam_detail'
    queryset = Quiz.objects.all()

class ExamUpdate(generic.UpdateView):
    template_name = 'exam_material/exam_update.html'
    form_class = ExamRegistrationForm
    model = Quiz
    context_object_name = 'exam_update'
    success_url = reverse_lazy('exam_material:exam-list')

    def form_valid(self, form) -> HttpResponse:
        # print(form.cleaned_data)
        self.object = form.save(commit=False)
        level_section = form.cleaned_data['levelSection']
        self.object.exam_section = level_section
        subject = self.object.subject
        title = self.object.title
        self.object.save()
        
        print(level_section)
        messages.success(self.request, f"Exam name: '{title}' was updated successfully. Subject: '{subject}'")

        return super().form_valid(form)

class ExamDelete(generic.DeleteView):
    template_name = 'exam_material/exam_delete.html'
    model = Quiz
    context_object_name = 'exam_delete'
    success_url = reverse_lazy('exam_material:exam-list')