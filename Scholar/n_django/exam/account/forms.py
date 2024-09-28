from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Student, Subject, Teacher , Staff, Role, Level, LevelSection, StaffPosition


#student registration form
class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        # widget = forms.CheckboxSelectMultiple(attrs={'class':'form-control', 'placeholder': 'Subjects'}),
        required = True
    )

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

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirmation'}))


    role = forms.CharField(label='Role',
        widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Student) #disabled=True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'role', 'subjects', 'level', 'levelSection']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['levelSection'].queryset  = LevelSection.objects.none()

        if 'level' in self.data:
            try:
                level_id = int(self.data.get('level'))
                self.fields['levelSection'].queryset = LevelSection.objects.filter(level_id=level_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Level queryset
        elif self.instance.pk:
            self.fields['levelSection'].queryset = self.instance.level.levelsection_set


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['student_subject'].queryset = Subject.objects.none()

        # if 'student_subject' in self.data:
        #     self.fields['student_subject'].queryset = Subject.objects.all()

        # elif self.instance.pk:
        #     self.fields['student_subject'].queryset = Subject.objects.all().filter(pk=self.instance.subjects.pk)


    def save(self):
        user = super().save(commit=False)
        user.role = Role.Student
        user.save()
        student = Student.objects.create(user=user, student_level=self.cleaned_data.get('level'), student_section=self.cleaned_data.get('levelSection')) #create
        student.student_subject.add(*self.cleaned_data.get('subjects')) #many to many field
        return student

#teacher registration form
class TeacherRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required = True
    )

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

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirmation'}))

    role = forms.CharField(label='Role', 
        widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Teacher)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'role' , 'subjects', 'level', 'levelSection']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['levelSection'].queryset  = LevelSection.objects.none()

        if 'level' in self.data:
            try:
                level_id = int(self.data.get('level'))
                self.fields['levelSection'].queryset = LevelSection.objects.filter(level_id=level_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Level queryset
        elif self.instance.pk:
            self.fields['levelSection'].queryset = self.instance.level.levelsection_set

    def save(self):
        user = super().save(commit=False)
        user.role = Role.Teacher
        user.save()
        teacher = Teacher.objects.create(user=user, teacher_level=self.cleaned_data.get('level'), teacher_section=self.cleaned_data.get('levelSection'))
        '''the * operator can be used to capture an unlimited number of positional arguments given to the function.
        These arguments are captured into a tuple.'''
        teacher.teacher_subject.add(*self.cleaned_data.get('subjects')) 
        return teacher

#staff registration form
class StaffRegisterationForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )

    position = forms.ModelChoiceField(
        queryset=StaffPosition.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Position'}), 
        required = True
    )

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirmation'}))

    role = forms.CharField(label='Role', 
            widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Staff)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'role' , 'position']
        
    def save(self):
        user = super().save(commit=False)
        user.role = Role.Staff
        user.save()
        staff = Staff.objects.create(user=user,  staff_position=self.cleaned_data.get('position'))
        return staff


class SubjectRegistrationForm(ModelForm):
    subject = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Subject'}) )
    class Meta:
        model = Subject
        fields = ['subject']

class LevelRegistrationForm(ModelForm):
    level = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Class'}) )
    class Meta:
        model = Level
        # this name shows in form
        fields = ['level'] 

class LevelSectionRegisrationForm(ModelForm):
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Class'}), 
        required = True
    )
    section = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Section'}) )
    class Meta:
        model = LevelSection
        fields = ['level','section']

class StaffPositionRegistrationForm(ModelForm):
    position = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Position'}) )
    class Meta:
        model = StaffPosition
        fields = ['position']

class StudentLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

    # to show in the terminal user entered value in the login form 
    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #     print("Username is:", username)
    #     print("Password is:", password)
    #     return cleaned_data
    
# def my_view(request):
#     print("View function is executing...")
#     if request.method == 'POST':
#         print("HTTP method is 'POST'")
#         form = StudentLoginForm(request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             username = form.cleaned_data['username']
#             print("Username is:", username)
#         else:
#             print("Form is not valid")


class TeacherLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))

class StaffLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))