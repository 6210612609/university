from django.contrib import admin

# Register your models here.

from .models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "maxquantity", "semester", "year")

class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ("courses",)

admin.site.register(Course, CourseAdmin)