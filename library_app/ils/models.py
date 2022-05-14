from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from time import timezone
from random import randrange

class Reader(models.Model):
    one_year_from_today = timezone.now() + timedelta(days=364)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library_card_number = models.CharField(max_length=9, unique=True)
    registration_date = models.DateField(auto_now_add=True)
    membership_end_date = models.DateField(default=one_year_from_today)

    @property
    def is_active_member(self):
        return self.membership_end_date >= timezone.now() or self.membership_end_date is None

class Librarian(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"[{self.id}] {self.last_name}, {self.first_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"[{self.id}] {self.name}"

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}] {self.name}  ({self.author.first_name} {self.author.last_name}) "

# TODO: Tag
# TODO: Rating
