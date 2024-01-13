from django.views import generic
from account.forms import TeacherRegistrationForm
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from account.models import Student, Teacher, Staff
from account.forms import StudentRegistrationForm, TeacherRegistrationForm
from main.forms import TeacherUpdateForm, StaffUpdateForm, StudentUpdateForm

from .forms import * 

class Index(generic.TemplateView):
    template_name = 'main/index.html'

class StudentPage(generic.TemplateView):
    template_name = 'main/student_page.html'

class TeacherPage(generic.TemplateView):
    template_name = 'main/teacher_page.html'

class StaffPage(generic.TemplateView):
    template_name = 'main/staff_page.html'
# class AfterTeacherLogin(generic.FormView):
#     template_name = 'account/teacher_login.html'
#     form_class = TeacherRegistrationForm
#     context_object_name = 'user_teacher_username'
#     success_url = reverse_lazy('main:after_teacher_login')

def staffNoticeBoard(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'main/staff_notice_board.html',context)

def teacherNoticeBoard(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'main/teacher_notice_board.html',context)

def staffNoticeView(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'main/staff_notice_view.html',context)

def teacherNoticeView(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'main/teacher_notice_view.html',context)

def studentNoticeBoard(request):
    forums=Forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'main/student_notice_board.html',context)


def staffCreateNotice(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:staff-notice-board')
    context ={'form':form}
    return render(request,'main/staff_create_notice.html',context)

def teacherCreateNotice(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:teacher-notice-board')
    context ={'form':form}
    return render(request,'main/teacher_create_notice.html',context)
 
def commentNotice(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:student-notice-board')
    context ={'form':form}
    return render(request,'main/comment_notice.html',context)


#For student
class StudentList(generic.ListView):
    template_name = 'main/student_list.html'
    model = Student
    context_object_name = 'student_list'
    queryset = Student.objects.all()

class StudentDetail(generic.DetailView):
    template_name = 'main/student_detail.html'
    model= Student
    context_object_name = 'student_detail'
    queryset = Student.objects.all()

class StudentUpdate(generic.UpdateView):
    template_name = 'main/student_update.html'
    form_class = StudentUpdateForm
    model = User
    context_object_name = 'student_update'
    success_url = reverse_lazy('main:student-page')

    
class StudentDelete(generic.DeleteView):
    template_name = 'main/student_delete.html'
    model = User
    context_object_name = 'student_delete'
    success_url = reverse_lazy('main:student-list')


#For teacher
class TeacherList(generic.ListView):
    template_name = 'main/teacher_list.html'
    model = Teacher
    context_object_name = 'teacher_list'
    queryset = Teacher.objects.all()
    

class TeacherDetail(generic.DetailView):
    template_name = 'main/teacher_detail.html'
    model= Teacher
    context_object_name = 'teacher_detail'
    queryset = Teacher.objects.all()

class TeacherUpdate(generic.UpdateView):
    template_name = 'main/teacher_update.html'
    form_class = TeacherUpdateForm
    model = User
    context_object_name = 'teacher_update'
    success_url = reverse_lazy('main:teacher-page')

    

class TeacherDelete(generic.DeleteView):
    template_name = 'main/teacher_delete.html'
    model = User
    context_object_name = 'teacher_delete'
    success_url = reverse_lazy('main:teacher-list')

#For staff
class StaffList(generic.ListView):
    template_name = 'main/staff_list.html'
    model = Staff
    context_object_name = 'staff_list'
    queryset = Staff.objects.all()
    

class StaffDetail(generic.DetailView):
    template_name = 'main/staff_detail.html'
    model= Staff
    context_object_name = 'staff_detail'
    queryset = Staff.objects.all()

class StaffUpdate(generic.UpdateView):
    template_name = 'main/staff_update.html'
    form_class = StaffUpdateForm
    model = User
    context_object_name = 'staff_update'
    success_url = reverse_lazy('main:staff-page')



class StaffDelete(generic.DeleteView):
    template_name = 'main/staff_delete.html'
    model = User
    context_object_name = 'staff_delete'
    success_url = reverse_lazy('main:staff-list')