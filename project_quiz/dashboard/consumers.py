import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class LeaderBoardWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "connected successfully."}))
        self.quiz_code = self.scope['url_route']['kwargs']['quiz_code']
        cache.set("%s_leader_board_channel" % self.quiz_code,
                  self.channel_name, (5 * 60))

    async def disconnect(self, code):
        cache.delete("%s_leader_board_channel" % self.quiz_code)

    async def receive(self, text_data):
        pass

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def send_score(self, event):
        message = event["score"]
        await self.send(text_data=json.dumps({"score": message}))

    async def close_connection(self, event):
        await self.close()
