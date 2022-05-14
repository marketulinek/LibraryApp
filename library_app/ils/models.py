from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from random import randrange

class Reader(models.Model):
    one_year_from_today = timezone.now() + timezone.timedelta(days=364)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library_card_number = models.CharField(max_length=9, unique=True)
    registration_date = models.DateField(auto_now_add=True)
    membership_end_date = models.DateField(default=one_year_from_today)

    @property
    def is_active_member(self):
        return self.membership_end_date >= timezone.now().date() or self.membership_end_date is None

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

@receiver(post_save, sender=User)
def create_reader(sender, instance, created, **kwargs):

    if created:
        # Generating unique nine-digit number
        card_number_exist = True
        while card_number_exist:

            new_card_number = ''
            for i in range(9):
                new_card_number += str(randrange(10))

            card_number_exist = Reader.objects.filter(library_card_number=new_card_number).exists()
        else:
            Reader.objects.create(user=instance,library_card_number=new_card_number)