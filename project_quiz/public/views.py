from django.views.generic import ListView, TemplateView
from quiz.models import Quiz
from django.core.cache import cache


class QuizListView(ListView):
    model = Quiz
    template_name = "public/quiz_list.html"
    context_object_name = "inactive_quizes"

    def get_queryset(self):
        return Quiz.objects.filter(is_active=False)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["live_quizes"] = Quiz.objects.filter(is_active=True)
        return context


class QuizView(TemplateView):
    template_name = "public/quiz.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["quiz"] = cache.get_or_set(
            "%s_quiz" % self.kwargs['quiz_code'],
            Quiz.objects.get(code=self.kwargs['quiz_code']),
            (60 * 5)
        )
        return context
