from django.contrib import admin
from django.db.models import F
from .models import Student, Order, Topic, Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'price', 'hours', 'for_everyone')

    def add_50_to_hours(self, request, queryset):
        queryset.update(hours = F('hours') + 10)
    admin.site.add_action(add_50_to_hours, "add_50_to_hours")

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'upper_case_name', 'city')

    def upper_case_name(self, obj):
        return obj.first_name.upper() + " " + obj.last_name.upper()

    upper_case_name.short_description = 'Student Full Name'

# Register your models here.
admin.site.register(Topic)
admin.site.register(Order)
# admin.site.register(Course)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
