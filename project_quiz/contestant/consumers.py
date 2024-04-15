from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from quiz.models import Quiz, Question, Answer
import json
from django.core.cache import cache
from channels.layers import get_channel_layer


class ContestantWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.quiz_code = self.scope['url_route']['kwargs']['quiz_code']
        self.player_name = self.scope['url_route']['kwargs']['name']
        self.que_count = 0
        self.questions = []
        self.quiz_res = {}
        self.score = {"answered_question": 0, "correct_answers": 0,
                      "incorrect_answers": 0}
        try:
            self.quiz = await self.get_quiz(self.quiz_code)
            if not self.quiz.is_active:
                await self.send(json.dumps({"message": "Quiz is not live."}))
                await self.close()
            else:
                await self.channel_layer.group_add(self.quiz_code,
                                                   self.channel_name)
                self.questions = await self.get_questions()
                self.answers = await self.get_answers()
                await self.message_leaderboard(
                    "%s joined the Quiz." % self.player_name)
                await self.send_question(self.que_count)
        except Quiz.DoesNotExist:
            await self.send(json.dumps({'message': 'Quiz not found'}))
            await self.close()

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.quiz_code, self.channel_name)
        quiz_res_combined = cache.get_or_set(
            "%s_result" % self.quiz_code, {}, (self.quiz.time * 60)*2)
        quiz_res_combined[self.player_name] = self.quiz_res
        cache.set("%s_result" % self.quiz_code,
                  quiz_res_combined, (self.quiz.time * 60)*2)
        if self.que_count == len(self.questions):
            await self.message_leaderboard(
                "%s Completed the Quiz." % self.player_name)
        else:
            await self.message_leaderboard(
                "%s left the Quiz." % self.player_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if self.questions[self.que_count].id != int(data['question_id']):
            await self.send(json.dumps({"message": "Something went wrong."}))
            await self.close()
        else:
            self.quiz_res[data['question_id']] = data['option_id']
            print(data)
            self.score["answered_question"] = self.que_count + 1
            await self.check_answer(data['question_id'], data['option_id'])
            score_combined = cache.get_or_set(
                "%s_score_board" % self.quiz_code, {}, (self.quiz.time * 60)*2)
            score_combined[self.player_name] = self.score
            cache.set("%s_score_board" % self.quiz_code,
                      score_combined, (self.quiz.time * 60)*2)
            self.que_count += 1
            await self.send_score(score_combined)
            await self.message_leaderboard(
                "%s answered the question." % self.player_name)
            await self.send_question(self.que_count)

    @database_sync_to_async
    def get_quiz(self, quiz_code):
        quiz = cache.get_or_set("%s_quiz" % quiz_code,
                                Quiz.objects.get(code=quiz_code),
                                (60 * 24))
        return quiz

    @database_sync_to_async
    def get_questions(self):
        que = cache.get_or_set(
            "%s_question_set" % self.quiz_code,
            Question.objects.filter(
                quiz=self.quiz).prefetch_related('option_set'), (60 * 24))
        return list(que)

    @database_sync_to_async
    def get_answers(self):
        ans = cache.get_or_set("%s_answer_set" % self.quiz_code,
                               Answer.objects.filter(question__quiz=self.quiz),
                               (60 * 24))
        return ans

    async def send_question(self, q_num):
        if q_num < len(self.questions):
            data = {"question_id": self.questions[q_num].id,
                    "question": self.questions[q_num].question}
            opt = {}
            for item in self.questions[q_num].option_set.all():
                opt[item.id] = item.value
            data['options'] = opt
            await self.send(json.dumps(data))
        else:
            await self.send(json.dumps({"message": "Quiz Completed",
                                        "score": self.score}))
            await self.close()

    @database_sync_to_async
    def check_answer(self, que_id, opt_id):
        que = self.answers.get(question=que_id)
        if que.answer.id == int(opt_id):
            self.score["correct_answers"] += 1
        else:
            self.score["incorrect_answers"] += 1

    async def message_group(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def disconnect_group(self, event):
        await self.close()

    async def message_leaderboard(self, message):
        leaderboard_chl = cache.get(
            "%s_leader_board_channel" % self.quiz_code)
        if leaderboard_chl is not None:
            channel_layer = get_channel_layer()
            await channel_layer.send(leaderboard_chl, {
                "type": "chat.message",
                "message": message,
            })
        else:
            print("No channel for leaderboard open.")

    async def send_score(self, score):
        leaderboard_chl = cache.get(
            "%s_leader_board_channel" % self.quiz_code)
        if leaderboard_chl is not None:
            channel_layer = get_channel_layer()
            await channel_layer.send(leaderboard_chl, {
                "type": "send.score",
                "score": score,
            })
        else:
            print("No channel for leaderboard open.")
