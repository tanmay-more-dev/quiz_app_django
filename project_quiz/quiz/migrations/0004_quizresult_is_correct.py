# Generated by Django 5.0.2 on 2024-03-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]