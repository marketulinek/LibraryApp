from django.db import models
from django.contrib.auth.models import User

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

    reader = models.ForeignKey(User, on_delete=models.RESTRICT) # Later switch to Reader
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    book_available_at = models.DateTimeField(null=True, blank=True)
    termination_type = models.CharField(max_length=10, choices=TERMINATION_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"[#{self.id}] {self.book.name} (reader: {self.reader.username})"

    class Meta:
        get_latest_by = "created_at"

# TODO: Tag
# TODO: Rating
