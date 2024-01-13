from django.db import models
from account.models import User
from account.models import Subject, LevelSection, Level
#for translation
# from django.utils.translation import gettext_lazy as _

# class Category(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self) -> str:
#         return self.name

SCALE = (
        ('fundamental', ('Fundamental')),
        ('beginner', ('Beginner')),
        ('intermediate', ('Intermediate')),
        ('advanced', ('Advanced')),
        ('expert', ('Expert'))
    )

#verbose name allows to name the name of the field in the admin as you want 
class Quiz(models.Model):
    title = models.CharField(max_length=255, default=('New Exam'), verbose_name=('Exam Title'))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default='Subject not selected')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='exam_level', null=True)
    exam_section = models.ForeignKey(LevelSection, on_delete=models.CASCADE, related_name='exam_level_section', null=True)
    numberOfQuestions = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    time = models.PositiveIntegerField(help_text="duration of the exam")
    scoreToPass = models.PositiveIntegerField()
    # difficulty = models.CharField(max_length=70, choices=SCALE, default='fundamental', verbose_name=("Difficulty"))

    def __str__(self) -> str:
        return f"{self.subject}: {self.title}"

    def get_questions(self):
        return self.question_set.all()[:self.numberOfQuestions]
    
    class Meta:
        verbose_name = ('Quiz')
        verbose_name_plural = ('Quizzes')
        ordering = ['id'] #orders according to the id


class Updated(models.Model):
    date_updated = models.DateTimeField(verbose_name=('Last Updated'), auto_now=True )

    class Meta:
        abstract = True


class Question(Updated):
    
    TYPE = (
        (0, ('Multiple Choice')),
    )

    exam_name = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name=("Exam name"))
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name=("Type of Question"))
    title = models.CharField(max_length=1000, verbose_name=("Question"))
    # difficulty = models.IntegerField(choices=SCALE, default=0, verbose_name=_("Difficulty"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=("Date Created"))
    # is_active = models.BooleanField(default=False, verbose_name=_("Active Status"))

    def __str__(self):
        return str(self.title)

    def get_answers(self):
        return self.answer_set.all()
    
    class Meta:
        verbose_name = ('Question')
        verbose_name_plural = ('Questions')
        ordering = ['id']


class Answer(Updated):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, verbose_name=("Answer"))
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"question: {self.question}, answer: {self.answer_text}, correct: {self.correct}"
    
    class Meta:
        verbose_name = ("Answer")
        verbose_name_plural = ("Answers")
        ordering = ['id']


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    exam_name = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    

    def __str__(self) -> str:
        return str(self.user)