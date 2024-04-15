from django.db import models
import time
from channels.layers import get_channel_layer
from threading import Thread
from asgiref.sync import async_to_sync
from django.core.cache import cache


class Quiz(models.Model):
    title = models.CharField(max_length=75)
    time = models.PositiveIntegerField(help_text="Quiz time in minutes.")
    code = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        cache.delete("%s_quiz" % self.code)
        if self.is_active:
            Thread(target=quiz_timer, args=(self.time, self.code)).start()
        return super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-id']

    def __str__(self) -> str:
        return self.question


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'option'
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ['-id']

    def __str__(self) -> str:
        return self.value


class QuizResult(models.Model):
    name = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer = models.ForeignKey(Option, on_delete=models.PROTECT)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_result'
        verbose_name = 'result'
        verbose_name_plural = 'results'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        db_table = 'answer'
        verbose_name = "answer"
        verbose_name_plural = "answers"

    def __str__(self):
        return str(self.question)


#  Rearrange later...
def quiz_timer(count, code):
    time.sleep(count*60)
    quiz = Quiz.objects.get(code=code)
    quiz.is_active = False
    quiz.save()
    chl = get_channel_layer()
    leaderboard = cache.get("%s_leader_board_channel" % code)
    print(leaderboard)
    try:
        async_to_sync(chl.group_send)(
            code, {'type': 'message_group', 'message': 'Time Up. Quiz Over.'})
        async_to_sync(chl.group_send)(code, {'type': 'disconnect.group'})
    except KeyError:
        pass
    if leaderboard is not None:
        async_to_sync(chl.send)(
            leaderboard, {
                "type": "chat.message",
                "message": "Quiz is over!"
            }
        )
        async_to_sync(chl.send)(
            leaderboard, {
                "type": "close.connection"
            }
        )

    result = cache.get("%s_result" % code)
    list_obj = []
    que_list = Question.objects.filter(quiz=quiz)
    opt_list = Option.objects.filter(question__in=que_list)
    ans_list = Answer.objects.filter(question__quiz=quiz)
    for key, value in result.items():
        name = key
        for key, value in value.items():
            if ans_list.get(question=key).answer == opt_list.get(id=value):
                correct = True
            else:
                correct = False
            print(correct)
            list_obj.append(QuizResult(
                name=name, quiz=quiz, question=que_list.get(id=key),
                answer=opt_list.get(id=value), is_correct=correct))
    QuizResult.objects.bulk_create(list_obj)

    cache.delete("%s_result" % code)
    cache.delete("%s_quiz" % code)
    cache.delete("%s_question_set" % code)
    cache.delete("%s_answer_set" % code)
    cache.delete("%s_score_board" % code)
