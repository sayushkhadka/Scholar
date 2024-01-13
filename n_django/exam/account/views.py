from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

from django.contrib import messages

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from account.models import Staff, Student, Teacher, Subject, User, Level, LevelSection, StaffPosition, Role 
from .forms import StaffLoginForm, StudentRegistrationForm, SubjectRegistrationForm, TeacherLoginForm, TeacherRegistrationForm, StaffRegisterationForm, StudentLoginForm, LevelRegistrationForm, LevelSectionRegisrationForm, StaffPositionRegistrationForm
from exam import settings


#student registration
class StudentRegistration(generic.CreateView):
    template_name = 'account/student_registration_form.html'
    form_class = StudentRegistrationForm
    model = Student
    success_url = reverse_lazy('account:student-registration')

    # def multiple_subjects(self, request):
    #     form = StudentRegistrationForm(instance=Student.objects.first())
    #     if request.is_ajax():
    #         term = request.GET.get('term') #'term' gives current typed letter in ajax to fetch the typed letter 
    #         subjects = Subject.objects.all().filter(title__icontains=term)
    #         return JsonResponse(list(subjects.values()), safe=False)
    #     if request.method == 'POST':
    #         form = StudentRegistrationForm(request.POST, instance=Student.objects.first())
    #         if form.is_valid():
    #             form.save()
    #             return redirect('account:student-registration')
    #     return render(request, 'account:student-registration', {'form': form})

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        user = self.object.user
        # username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
    
        subjects = list(self.object.student_subject.values_list('subject', flat=True))
        

        subject = f'Login credentials, {user.get_role_display()}.'
        messageFromEmail = f'Hello {user.get_full_name()}. Welcome to Scholar.\nYour login credentials are as follows:\nUsername: {user.username}\nPassword: {password}\nSubjects: {subjects}'
        fromEmail = settings.EMAIL_HOST_USER
        toEmail = [user.email]
        send_mail(subject, messageFromEmail, fromEmail, toEmail, fail_silently=True)

        messages.success(self.request, f'{user.username} was registered successfully. The login credentials have been delivered to {user.username}.')
        return HttpResponseRedirect(self.get_success_url())
        
     
#teacher registration
class TeacherRegistration(generic.CreateView):
    template_name = 'account/teacher_registration_form.html'
    form_class = TeacherRegistrationForm
    model = Teacher
    success_url = reverse_lazy('account:teacher-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        user = self.object.user
        # username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
    
        subjects = list(self.object.teacher_subject.values_list('subject', flat=True))
        

        subject = f'Login credentials, {user.get_role_display()}.'
        messageFromEmail = f'Hello {user.get_full_name()}. Welcome to Scholar.\nYour login credentials are as follows:\nUsername: {user.username}\nPassword: {password}\nSubjects: {subjects}'
        fromEmail = settings.EMAIL_HOST_USER
        toEmail = [user.email]
        send_mail(subject, messageFromEmail, fromEmail, toEmail, fail_silently=True)

        messages.success(self.request, f'{user.username} was registered successfully. The login credentials have been delivered to {user.username}.')
        return HttpResponseRedirect(self.get_success_url())

def load_level_section(request):
    level_id = request.GET.get('level_id')
    sections = LevelSection.objects.filter(level_id=level_id)
    return render(request, 'account/level_section.html', {'sections': sections})


    
#subject registration
class SubjectRegistration(generic.CreateView):
    template_name = 'account/subject_registration_form.html'
    form_class = SubjectRegistrationForm
    model = Subject
    success_url = reverse_lazy('account:subject-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        subject = self.object.subject
        messages.success(self.request, f'Subject {subject} was registered successfully.')

        return super().form_valid(form)

#Class registration 
class LevelRegistration(generic.CreateView):
    template_name = 'account/level_registration_form.html'
    form_class = LevelRegistrationForm
    model = Level
    success_url = reverse_lazy('account:level-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        level = self.object.level
        messages.success(self.request, f'Class {level} was registered successfully.')

        return super().form_valid(form)


#class section
class LevelSectionRegistration(generic.CreateView):
    template_name = 'account/level_section_registration_form.html'
    form_class = LevelSectionRegisrationForm
    model = LevelSection
    success_url = reverse_lazy('account:level-section-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        section = self.object.section
        messages.success(self.request, f'Section {section} was registered successfully.')

        return super().form_valid(form)

#staff position registration
class StaffPositionRegistration(generic.CreateView):
    template_name = 'account/staff_position_registration_form.html'
    form_class = StaffPositionRegistrationForm
    model = StaffPosition
    success_url = reverse_lazy('account:staff-position-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        position = self.object.position
        messages.success(self.request, f"Staff position '{position}' was registered successfully.")

        return super().form_valid(form)



#staff registration
class StaffRegistration(generic.CreateView):
    template_name = 'account/staff_registration_form.html'
    form_class = StaffRegisterationForm
    model = Staff
    success_url= reverse_lazy('account:staff-registration')

    def form_valid(self, form) -> HttpResponse:
        self.object=form.save()
        user = self.object.user
        # username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
    
        # position = self.object.staff_position
        

        subject = f'Login credentials, {user.get_role_display()}.'
        messageFromEmail = f'Hello {user.get_full_name()}. Welcome to Scholar.\nYour login credentials are as follows:\nUsername: {user.username}\nPassword: {password}\nPosition: {self.object.staff_position}'
        fromEmail = settings.EMAIL_HOST_USER
        toEmail = [user.email]
        send_mail(subject, messageFromEmail, fromEmail, toEmail, fail_silently=True)

        messages.success(self.request, f'{user.username} was registered successfully. The login credentials have been delivered to {user.username}.')
        return HttpResponseRedirect(self.get_success_url())

#student list
class StudentList(generic.ListView):
    template_name = 'account/student_list.html'
    model = Student
    context_object_name = 'student_list'
    queryset = Student.objects.all()

#teacher list
class TeacherList(generic.ListView):
    template_name = 'account/teacher_list.html'
    model = Teacher
    context_object_name = 'teacher_list'
    queryset = Teacher.objects.all()

#staff list
class StaffList(generic.ListView):
    template_name = 'account/staff_list.html'
    model = Teacher
    context_object_name = 'staff_list'
    queryset = Staff.objects.all()

#student login
class StudentLogin(generic.FormView):
    template_name = 'account/student_login.html'
    form_class = StudentLoginForm
    context_object_name = 'user_student_username'
    success_url = reverse_lazy('main:student-page')

    def form_valid(self, form) -> HttpResponse:
        
        #form.cleaned_data returns a dictionary of validated form input fields and their values, where string primary keys are returned as objects.
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        # print('Username:', username)

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_student:
                login(self.request, user)
                return super().form_valid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context.update({
            'error': "Either username or password is invalid."
        })
        return self.render_to_response(context)

#teacher login
class TeacherLogin(generic.FormView):
    template_name = 'account/teacher_login.html'
    form_class = TeacherLoginForm
    context_object_name = 'user_teacher_username'
    success_url = reverse_lazy('main:teacher-page')

    def form_valid(self, form) -> HttpResponse:
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_teacher:
                login(self.request, user)
                return super().form_valid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context.update({
            'error': "Either username or password is invalid."
        })
        return self.render_to_response(context)

#staff login
class StaffLogin(generic.FormView):
    template_name = 'account/staff_login.html'
    form_class = StaffLoginForm
    context_object_name = 'user_staff_username'
    success_url = reverse_lazy('main:staff-page')

    def form_valid(self, form) -> HttpResponse:
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_staff1:
                login(self.request, user)
                return super().form_valid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context.update({
            'error': "Either username or password is invalid."
        })
        return self.render_to_response(context)
    


# class AfterTeacherLogin(generic.FormView):
#     template_name = 'account/student_registration_form.html'
#     form_class = StudentRegistrationForm
#     context_object_name = 'user_student_username1'
#     success_url = reverse_lazy('main:after_teacher_login')

# class AfterTeacherLogin(generic.TemplateView):
#     template_name = 'account/after_teacher_login.html'


class UserLogOut(generic.View):

    def logout_request(self, request):
        logout(request)
        # user = self.object.user
        messages.success(self.request, f' you have been logged out successfully.')
        return redirect('main:index')
    
