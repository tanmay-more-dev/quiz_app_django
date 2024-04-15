from django.urls import path
from .consumers import LeaderBoardWebSocketConsumer


websocket_urlpatterns = [
    path('ws/quiz/live/<str:quiz_code>/',
         LeaderBoardWebSocketConsumer.as_asgi()),
]
