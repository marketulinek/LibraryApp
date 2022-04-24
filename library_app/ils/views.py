from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView
from . import models

class IndexView(TemplateView):
    template_name = 'index.html'

class AuthorListView(ListView):
    template_name = 'author/author_list.html'
    model = models.Author

class AuthorDetailView(DetailView):
    template_name = 'author/author_detail.html'
    model = models.Author

class AuthorCreateView(CreateView):
    template_name = 'author/author_create.html'
    model = models.Author
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('author_list')

class BookListView(ListView):
    template_name = 'book/book_list.html'
    model = models.Book

class BookDetailView(DetailView):
    template_name = 'book/book_detail.html'
    model = models.Book

class BookFormView(CreateView):
    model = models.Book
    template_name = 'book/book_form.html'
    fields = ["name", "author", "publisher", "year", "description"]
    success_url = reverse_lazy('book_form_confirmation')

class BookFormConfirmationView(TemplateView):
    template_name = 'book/book_form_confirmation.html'