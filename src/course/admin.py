from django.contrib import admin
from .models import Course, StudentProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester', 'units')
    filter_horizontal = ('prerequisites',) # برای انتخاب راحت‌تر پیش‌نیازها

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('passed_courses',)