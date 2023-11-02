from datetime import datetime

from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    email = models.EmailField(verbose_name='электронная почта')
    surname = models.CharField(max_length=50, verbose_name='фамилия')
    name = models.CharField(max_length=50, verbose_name='имя')
    middle_name = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Клиент: {self.email}.'

    def save(self, *args, **kwargs):
        if Client.objects.filter(user=self.user, email=self.email).exists():
            raise ValueError
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    REGULARITY_CHOICES = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    )

    mailing_time = models.DateTimeField(verbose_name='время рассылки')
    regularity = models.CharField(max_length=10, choices=REGULARITY_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус рассылки')
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='клиенты')
    mail_theme = models.TextField(max_length=100, verbose_name='тема письма')
    mail_text = models.TextField(max_length=350, verbose_name='тело письма')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    def __str__(self):
        return f'Рассылка {self.mail_theme}.'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    )

    timestamp = models.DateTimeField(default=datetime.now, verbose_name='дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    client = models.ManyToManyField(Client, related_name='logs', verbose_name='клиент')
    mailing_list = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='logs',
                                     verbose_name='рассылка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Лог: "{self.mailing_list}"'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
