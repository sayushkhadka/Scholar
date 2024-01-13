from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Question, Answer, Quiz
from account.models import Subject, Level, LevelSection

class ExamRegistrationForm(ModelForm):
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Class'}), 
        required = True
    )

    levelSection = forms.ModelChoiceField(
        queryset=LevelSection.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Section'}), 
        required = True
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Subject'}), 
        required = True
    )

    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Exam name'}) )
    numberOfQuestions = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'No of Questions(*Cannot be changed later*)'}))
    time = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Time (In minutes)'}))
    scoreToPass = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Score To Pass'}))

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['levelSection'].queryset  = LevelSection.objects.none()

        if 'level' in self.data:
            try:
                level_id = int(self.data.get('level'))
                self.fields['levelSection'].queryset = LevelSection.objects.filter(level_id=level_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['levelSection'].queryset = self.instance.level.levelsection_set

    class Meta:
        model = Quiz
        fields = ['level', 'levelSection', 'subject', 'title', 'numberOfQuestions', 'time', 'scoreToPass']


class QuestionForm(forms.ModelForm):
    exam_name = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Exam name'}), 
        required = True
    )
    # technique = forms.ModelChoiceField(
    #     queryset=Question.objects.values('technique'),
    #     widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Type of question'}), 
    #     required = True
    # )
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Question'}) )
    class Meta:
        model = Question
        fields = '__all__'
        # widgets = {
        #     'technique': forms.ModelChoiceField(
        #         queryset=Question.objects.all(),
        #         # attrs={
        #         #     'class': 'form-control'
        #         #     }
        #         ),
        # }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            'answer_text': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'correct': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }

AnswerFormSet = inlineformset_factory(
    Question, Answer, form = AnswerForm, extra = 1, can_delete=True, can_delete_extra=True
)
