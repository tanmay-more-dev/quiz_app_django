from django.urls import path
from .views import (HomeView, LeaderBoardView, QuizDetailView,
                    QuizCreateView, QuestionCreateView, QuestionDeleteView)


app_name = "dashboard"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("<str:code>/question/<int:pk>/delete/", QuestionDeleteView.as_view(),
         name="question_delete"),
    path("quiz/<str:code>/question/new/", QuestionCreateView.as_view(),
         name="question_create"),
    path("quiz/new/", QuizCreateView.as_view(), name="quiz_create"),
    path("<str:code>/", QuizDetailView.as_view(), name="quiz_detail"),
    path("leaderboard/<str:quiz_code>/", LeaderBoardView.as_view(),
         name="leaderboard"),
]
