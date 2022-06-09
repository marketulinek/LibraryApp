from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render     # for search box
from django.db.models import Q          # for search box
from . import models
from .forms import RegisterUserForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        num_of_reservations = models.BookReservation.objects.filter(book=self.kwargs['pk'], termination_type__isnull=True).count()
        context['reservation_queue'] = num_of_reservations

        if num_of_reservations == 0:
            context['can_be_reserved_until'] = timezone.now() + timezone.timedelta(days=5)
        elif self.request.user.is_authenticated:
            context['user_already_reserved'] = models.BookReservation.objects.filter(reader=self.request.user.reader, book=self.kwargs['pk'], termination_type__isnull=True).exists()

        return context

class BookFormView(CreateView):
    model = models.Book
    template_name = 'book/book_form.html'
    fields = ["name", "author", "publisher", "year", "description"]
    success_url = reverse_lazy('book_form_confirmation')

class BookFormConfirmationView(TemplateView):
    template_name = 'book/book_form_confirmation.html'

class CatalogueView(ListView):
    template_name = 'catalogue/catalogue.html'
    model = models.Book

class LibraryRulesView(TemplateView):
    template_name = 'for_readers/library_rules.html'

class FAQView(TemplateView):
    template_name = 'for_readers/faq.html'

class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = "registration/register.html"


# ------------------------------
#         ACTION  VIEWS
# ------------------------------

class MakeReservationView(View):

    def post(self, request, *args, **kwargs):

        pk_book = self.kwargs['pk']
        chosen_book = models.Book.objects.get(pk=pk_book)
        # Todo: if book is available (not exist open reservation for a book) -> fill in 'available_at'

        try:
            models.BookReservation(reader=request.user.reader, book=chosen_book).save()
            messages.success(request, 'Reservation was successfully created.')

        except models.Reader.DoesNotExist:
            messages.error(request, 'Permission denied. You are not a reader.')

        return HttpResponseRedirect(reverse_lazy('book_detail', kwargs={'pk': pk_book}))




# ------------------------------
#         SEARCH BOX
# ------------------------------

class SearchResultsView(TemplateView):
    model = models.Book
    template_name = 'search_results.html'

# This function works well but it should be later extended to a class
def search_results(request):
    query = request.GET.get('query')
    results = models.Book.objects.filter( Q(name__icontains=query)|
                                          Q(author__first_name__icontains=query)|
                                          Q(author__last_name__icontains=query)
                                          )
    return render(request, 'search_results.html', {'query': query,
                                                   'results': results})