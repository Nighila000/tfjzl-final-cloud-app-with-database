from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# Inline for Lessons inside Course
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Inline for Choices inside Question
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


# Inline for Questions inside Course (optional use)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# Course Admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content']


# Lesson Admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)