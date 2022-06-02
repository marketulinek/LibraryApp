from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
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
    context_object_name = 'book'

class BookFormView(CreateView):
    model = models.Book
    template_name = 'book/book_form.html'
    fields = ["name", "author", "publisher", "year", "description"]
    success_url = reverse_lazy('book_form_confirmation')

class BookFormConfirmationView(TemplateView):
    template_name = 'book/book_form_confirmation.html'

class LibraryRulesView(TemplateView):
    template_name = 'for_readers/library_rules.html'

class FAQView(TemplateView):
    template_name = 'for_readers/faq.html'


# ------------------------------
#         ACTION  VIEWS
# ------------------------------

class MakeReservationView(View):

    def post(self, request, *args, **kwargs):

        try:
            pk_book = self.kwargs['pk']
            chosen_book = models.Book.objects.get(pk=pk_book)

            # Todo: if book is available (not exist open reservation for a book) -> fill in 'available_at'

            models.BookReservation(reader=request.user.reader, book=chosen_book).save()
            messages.success(request, 'Reservation was successfully created.')

        except models.Reader.DoesNotExist:
            messages.error(request, 'Permission denied. You are not a reader.')

        return HttpResponseRedirect(reverse_lazy('book_detail', kwargs={'pk': pk_book}))