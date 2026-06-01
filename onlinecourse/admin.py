from django.contrib import admin

# Import models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# Lesson inline inside Course
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Choice inline inside Question
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


# Question inline (optional but required by lab structure)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# Course admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Question admin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text']


# Lesson admin
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