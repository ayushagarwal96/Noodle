from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from .choices import *
import re, math
from collections import Counter
import numpy
import numpy.linalg

WORD = re.compile(r'\w+')


class Book(models.Model):
    user = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)
    sub_category = models.CharField(max_length=30, blank=True)
    cover = models.FileField(blank=True)
    image_url = models.CharField(max_length=300, blank=True)
    condition = models.IntegerField(choices=CONDITION_CHOICES, default=1)
    edition = models.CharField(max_length=30, blank=True)
    cost = models.IntegerField(default=200)
    # seller = models.ForeignKey(User)
    cost = models.IntegerField()
    buy_sell = models.IntegerField(choices=BUY_SELL_ENUM, default=1)

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return (self.title)

    @classmethod
    def get_cosine(cls, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    @classmethod
    def text_to_vector(cls, text):
        words = WORD.findall(text)
        return Counter(words)

    @staticmethod
    def nearest_neighbour(self, feature_array):
        distances_and_index = []
        index = 0
        for features in feature_array:
            a = numpy.array((features[0], features[1], features[2], features[3]))
            b = numpy.array((1.0, 1.0, 1.0, self.category))

            dist = numpy.linalg.norm(a - b)
            distances_and_index.append([dist, index])
            index += 1

            distances_and_index.sort()

        return  distances_and_index

    def recommend_books(self):
        other_books = Book.objects.exclude(pk=self.pk).all()
        books = []
        feature_array = []

        for book in other_books:
            books.append(book.__dict__)

        for book in other_books:
            a = Book.text_to_vector(book.author)
            b = Book.text_to_vector(self.author)
            f1 = Book.get_cosine(a, b)
            a = Book.text_to_vector(book.publisher)
            b = Book.text_to_vector(self.publisher)
            f2 = Book.get_cosine(a, b)
            a = Book.text_to_vector(book.sub_category)
            b = Book.text_to_vector(self.sub_category)
            f3 = Book.get_cosine(a, b)
            f4 = book.category
            feature_array.append([float(f1), float(f2), float(f3), float(book.category)])

        recommended_books = Book.nearest_neighbour(self, feature_array)
        resp = []
        print len(recommended_books)
        for book in recommended_books[:4]:
            resp.append(other_books[book[1]])

        return resp
