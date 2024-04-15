from django.contrib import admin
from .models import Question, Quiz, Option, QuizResult, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'is_active', 'code')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'value')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'question', 'answer', 'is_correct')
