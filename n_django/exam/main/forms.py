from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import Subject, Level, Role, LevelSection, User, Teacher

 
class CreateInForum(ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Who is posting?'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )
    topic = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Topic'}) )
    description = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Description'}) )
    
    class Meta:
        model= Forum
        fields = "__all__"

 
class CreateInDiscussion(ModelForm):

    forum = forms.ModelChoiceField(
        queryset=Forum.objects.all(),
        widget = forms.Select(attrs={'class':'form-control', 'placeholder': 'Class'}), 
        required = True
    )

    discuss = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Add your comment'}) )

    class Meta:
        model= Discussion
        # fields = "__all__"
        fields = ['forum', 'discuss']



#teacher update form
class TeacherUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )
    # username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    

    role = forms.CharField(label='Role', 
        widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Teacher)

    class Meta:
        model = User
        fields = [ 'first_name','last_name','email','role']


class StudentUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )
    # username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    

    role = forms.CharField(label='Role', 
        widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Student)

    class Meta:
        model = User
        fields = [ 'first_name','last_name','email','role']


class StaffUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}) )
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}) )
    # username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}) )
    

    role = forms.CharField(label='Role', 
        widget=forms.Select(choices=Role.role_choices, attrs={'class':'form-control', 'placeholder': 'Role'}), disabled=True, initial=Role.Staff)

    class Meta:
        model = User
        fields = [ 'first_name','last_name','email','role']


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.first_name = self.cleaned_data.get('first_name')
    #     user.last_name = self.cleaned_data.get('last_name')
    #     user.email = self.cleaned_data.get('email')
        
    #     user.save()


    
