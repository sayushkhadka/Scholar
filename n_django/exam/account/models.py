from django.contrib.auth.models import AbstractUser

from django.db import models

#for choosing roles(student, teacher, staff, admin)
class Role:
    Admin = 1
    Student = 2
    Teacher = 3
    Staff = 4
    NotSelected = 5
    
    role_choices = (
        (Admin, 'admin'),
        (Student, 'student'),
        (Teacher, 'teacher'),
        (Staff, 'staff'),
        (NotSelected, 'notSelected')
    )


class User(AbstractUser):

    # first_name = models.CharField(max_length=30, blank=False, null=False, default=None)
    # last_name = models.CharField(max_length=30, blank=False, null=False, default=None)
    # email = models.EmailField(max_length=250, blank=False, null=False, default=None)

    base_role = Role.NotSelected

    role = models.IntegerField('Role', choices=Role.role_choices, null=False, blank=False, default=base_role)


    @property
    def is_student(self):
        return self.role == Role.Student

    @property
    def is_teacher(self):
        return self.role == Role.Teacher
        
    @property
    def is_staff1(self):
        return self.role == Role.Staff
    
    def __str__(self) -> str:
        return f"{self.username}"


class Level(models.Model):
    level = models.PositiveIntegerField(blank=False, null=False, default=0)
    
    def __str__(self) -> str:
        return f"{self.level}"
    
class Subject(models.Model):
    subject = models.CharField(max_length=30, blank=True)
    # level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.subject

class LevelSection(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    section = models.CharField(max_length=30, help_text='Please use capital letters for section.')

    def __str__(self) -> str:
        return self.section.upper()

class StaffPosition(models.Model):
    position = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.position


class Student(models.Model):
    base_role = Role.Student
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    student_subject = models.ManyToManyField(Subject, related_name='student_subject')
    student_level = models.ForeignKey(Level, on_delete=models.CASCADE ,related_name='student_level', null=True)
    student_section = models.ForeignKey(LevelSection, on_delete=models.CASCADE, related_name='student_level_section', default=0)
    #role = models.IntegerField(choices=User.Role.role_choices, null=False, blank=False, default=User.Role.Student)

    # @property
    # def student_level(self):
    #     self.student_section.level

    def __str__(self) -> str:
        return self.user.username
    
    # def save(self, *args, **kwargs):
    #     print("Username is:", self.user.username)
    #     super().save(*args, **kwargs)



class Teacher(models.Model):
    base_role = Role.Teacher

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="teacher")
    teacher_subject = models.ManyToManyField(Subject, related_name='teacher_subject')
    teacher_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='teacher_level', null=True)
    teacher_section = models.ForeignKey(LevelSection, on_delete=models.CASCADE, related_name='teacher_level_section', default=0)
    #role = models.IntegerField(choices=Role.role_choices, default=base_role)

    def __str__(self) -> str:
        return self.user.username

class Staff(models.Model):
    base_role = Role.Staff

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff')
    staff_position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE, related_name='staff_position', default='staff')
    #role = models.IntegerField(choices=Role.role_choices, default=base_role)

    def __str__(self) -> str:
        return self.user.username


    