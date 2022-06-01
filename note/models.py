from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def complete_time():
    return datetime.now() + timedelta(days=1)


class Note(models.Model):
    """
    Заметки для ведения списка дел.
    """
    class Status(models.TextChoices):
        ACTIVE = 'AC', _('Активно')
        POSTPONED = 'PO', _('Отложено')
        COMPLETED = 'CO', _('Выполнено')

    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок'
    )
    note = models.TextField(verbose_name='Текст заметки')
    status = models.CharField(
        max_length=2,
        default=Status.ACTIVE,
        choices=Status.choices,
        verbose_name='Статус'
    )
    important = models.BooleanField(
        default=False,
        verbose_name='Важно'
    )
    public = models.BooleanField(
        default=False,
        verbose_name='Опубликовать'
    )
    complete_time = models.DateTimeField(
        default=complete_time,
        verbose_name='Срок выполнения'
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    """ Комментарии и оценки к записям """

    class Ratings(models.IntegerChoices):  # https://docs.djangoproject.com/en/4.0/ref/models/fields/#enumeration-types
        WITHOUT_RATING = 0, _('Без оценки')
        TERRIBLE = 1, _('Ужасно')
        BADLY = 2, _('Плохо')
        FINE = 3, _('Нормально')
        GOOD = 4, _('Хорошо')
        EXCELLENT = 5, _('Отлично')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Запись')  # default related_name='comment_set'
    rating = models.IntegerField(default=Ratings.WITHOUT_RATING, choices=Ratings.choices,
                                 verbose_name='Оценка')
