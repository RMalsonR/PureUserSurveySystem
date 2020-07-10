from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models

from .roles import Role


class QuestionType(Enum):
    TEXT = 'TEXT'
    TEST_SINGLE = 'TEST_SINGLE'
    TEST_SET = 'TEST_SET'

    @classmethod
    def as_choices(cls):
        return (
            (cls.TEXT.value, 'Вопрос с текстовым вариантом ответа'),
            (cls.TEST_SINGLE.value, 'Вопрос с выбором одного ответа'),
            (cls.TEST_SET.value, 'Вопрос с выбором нескольких ответов'),
        )


class User(AbstractUser):
    role = models.CharField(max_length=64, choices=Role.as_choices(), verbose_name='Роль пользователя',
                            default=Role.SURVEY_PARTICIPANT.value)

    def is_admin(self):
        return self.role == Role.ADMIN_ROLE.value

    def is_survey(self):
        return self.role == Role.SURVEY_PARTICIPANT.value

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(max_length=64, choices=QuestionType.as_choices(), verbose_name='Тип вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Poll(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название опроса')
    start_datetime = models.DateTimeField(auto_created=True, auto_now_add=True,
                                          verbose_name='Дата и время начала опроса')
    end_datetime = models.DateTimeField(auto_now_add=False, auto_created=False,
                                        verbose_name='Дата и время окончания опроса')
    description = models.TextField(verbose_name='Описание опроса')
    questions = models.ManyToManyField(Question, related_name='polls', verbose_name='Вопросы')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    is_anonymous = models.BooleanField(default=False, verbose_name='Ответ анонимный?')

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
