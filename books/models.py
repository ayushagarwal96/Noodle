from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from .choices import *


class Book(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)
    sub_category = models.CharField(max_length=30, blank=True)
    cover = models.FileField()
    condition = models.IntegerField(choices=CONDITION_CHOICES, default=1)
    edition = models.CharField(max_length=30, blank=True)
    cost = models.IntegerField()
    buy_sell = models.IntegerField(choices=BUY_SELL_ENUM, default=1)

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
