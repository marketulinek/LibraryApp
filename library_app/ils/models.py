from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from random import randrange


class Reader(models.Model):

    def get_one_year_from_today():
        return timezone.now() + timezone.timedelta(days=364)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library_card_number = models.CharField(max_length=9, unique=True)
    registration_date = models.DateField(auto_now_add=True)
    membership_end_date = models.DateField(default=get_one_year_from_today)

    @property
    def is_active(self):
        return self.membership_end_date >= timezone.now().date() or self.membership_end_date is None

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"

class Librarian(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    @property
    def is_active(self):
        return self.end_date >= timezone.now().date() or self.end_date is None

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

class BookReservation(models.Model):
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    FORFEITED = 'Forfeited'
    TERMINATION_CHOICES = (
        (COMPLETED, 'Reservation completed'),
        (CANCELLED, 'Reservation cancelled'),
        (FORFEITED, 'Reservation forfeited')
    )

    reader = models.ForeignKey(Reader, on_delete=models.RESTRICT)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    book_available_at = models.DateTimeField(null=True, blank=True)
    termination_type = models.CharField(max_length=10, choices=TERMINATION_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"[#{self.id}] {self.book.name} (reader: {self.reader.user.username})"

    class Meta:
        get_latest_by = "created_at"

# TODO: Tag
# TODO: Rating


# ------------------------------
#            SIGNALS
# ------------------------------

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