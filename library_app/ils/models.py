from django.db import models

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
