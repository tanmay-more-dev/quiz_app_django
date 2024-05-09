from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, TemplateView, DetailView,
                                  CreateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.models import Quiz, Question
from .forms import QuestionForm


class HomeView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = "dashboard/home.html"
    context_object_name = "quizes"


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "dashboard/confirm_delete.html"
    success_url = reverse_lazy('dashboard:home')
    context_object_name = "object_to_delete"

    def get_success_url(self) -> str:
        return reverse('dashboard:quiz_detail', kwargs={
            "code": self.kwargs['code']
        })


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "dashboard/question_form.html"
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        form.instance.quiz = Quiz.objects.get(code=self.kwargs['code'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('dashboard:quiz_detail', kwargs={
            "code": self.kwargs['code']
        })

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["code"] = self.kwargs['code']
        return context


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = '__all__'
    template_name = "dashboard/quiz_form.html"
    success_url = reverse_lazy('dashboard:home')


class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "dashboard/quiz_detail.html"
    context_object_name = "quiz"

    def get_object(self):
        return Quiz.objects.get(code=self.kwargs['code'])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.filter(
            quiz=self.get_object()).prefetch_related(
                'option_set').prefetch_related('answer_set')
        return context


class LeaderBoardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/leaderboard.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(code=self.kwargs['quiz_code'])
        context["quiz"] = quiz
        return context
