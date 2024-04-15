from django.urls import path
from .consumers import ContestantWebSocketConsumer
from dashboard.consumers import LeaderBoardWebSocketConsumer


websocket_urlpatterns = [
    path('ws/quiz/<str:name>/<str:quiz_code>/',
         ContestantWebSocketConsumer.as_asgi()),
    path('ws/quiz/<str:quiz_code>/leaderboard/live/',
         LeaderBoardWebSocketConsumer.as_asgi()),
]
