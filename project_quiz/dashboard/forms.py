from django import forms
from quiz.models import Question, Option


class QuestionForm(forms.ModelForm):
    option_one = forms.CharField(max_length=150)
    option_two = forms.CharField(max_length=150)
    option_three = forms.CharField(max_length=150)
    option_four = forms.CharField(max_length=150)

    class Meta:
        model = Question
        exclude = ('quiz',)

    def save(self, commit=True):
        print('working')
        que = super().save(commit)
        opts = [
            Option(question=que, value=self.cleaned_data['option_four']),
            Option(question=que, value=self.cleaned_data['option_three']),
            Option(question=que, value=self.cleaned_data['option_two']),
            Option(question=que, value=self.cleaned_data['option_one']),
        ]
        Option.objects.bulk_create(opts)
        return que
