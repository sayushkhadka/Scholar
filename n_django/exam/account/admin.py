from django.contrib import admin
#from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import User, Student, Subject, Teacher, Staff, Level, LevelSection, StaffPosition


class UserAdmin(UserAdmin):
    model = User

    fieldsets = (
        *UserAdmin.fieldsets,
        
        ('User role',{'fields': ('role',)}),
        # ('Add user',{'fields':('first_name', 'last_name', 'email')}),
    )

    

# print(UserAdmin.fieldsets)
admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Subject)
# admin.site.register(Level)
admin.site.register(LevelSection)
admin.site.register(Teacher)
admin.site.register(StaffPosition)
admin.site.register(Staff)




class LevelSectionModel(admin.TabularInline):
    model = LevelSection
    fields = [
            'section',
        ]

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    
    inlines = [LevelSectionModel,]

# admin.site.register(LevelAdmin)