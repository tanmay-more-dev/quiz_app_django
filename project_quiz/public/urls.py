from django.urls import path
from .views import QuizListView, QuizView


app_name = "public"

urlpatterns = [
    path('', QuizListView.as_view(), name="home"),
    path('quiz/<str:quiz_code>/', QuizView.as_view(), name="quiz"),
]
