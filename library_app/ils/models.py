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
        return self.end_date is None or self.end_date >= timezone.now().date()

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
    AVAILABLE = 'Available'
    RESERVED = 'Reserved'
    BORROWED = 'Borrowed'
    UNAVAILABLE = 'Unavailable'
    STATUS_CHOICES = (
        (AVAILABLE, 'Book Available'),
        (RESERVED, 'Book Reserved'),
        (BORROWED, 'Book Borrowed'),
        (UNAVAILABLE, 'Book Unavailable')
    )

    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}] {self.name}  ({self.author.first_name} {self.author.last_name}) "

class BookLoan(models.Model):

    reader = models.ForeignKey(Reader, on_delete=models.RESTRICT)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    @property
    def book_return_deadline(self):
        return self.created_at + timezone.timedelta(days=30)

    def __str__(self):
        return f"[#{self.id}] {self.book.name} (reader: {self.reader.user.username})"

    class Meta:
        get_latest_by = "created_at"

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

@receiver(pre_save, sender=BookReservation)
def create_loan_from_reservation(sender, instance, **kwargs):

    if instance.id is not None:
        old_instance = BookReservation.objects.get(id=instance.id)

        # If book reservation was completed
        if old_instance.termination_type is None and instance.termination_type == 'Completed':

            BookLoan.objects.create(reader=instance.reader, book=instance.book)

@receiver(pre_save, sender=BookLoan)
def update_book_available_field_in_reservation(sender, instance, **kwargs):

    if instance.id is not None:
        old_instance = BookLoan.objects.get(id=instance.id)

        # If book was returned
        if old_instance.returned_at is None and instance.returned_at is not None:

            # Get the oldest open reservation of the book
            br = BookReservation.objects.filter(book=instance.book,termination_type__isnull=True).order_by('created_at').first()

            if br:
                br.book_available_at = instance.returned_at
                br.save()