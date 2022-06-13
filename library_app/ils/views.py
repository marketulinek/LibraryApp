from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q          # for search box
from . import models, tables
from .forms import RegisterUserForm, AuthorForm, BookForm, PublisherForm
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
import ils.tables as tables
from django_tables2 import SingleTableView


class IndexView(TemplateView):
    template_name = 'index.html'

class AuthorListView(ListView):
    template_name = 'author/author_list.html'
    model = models.Author

class AuthorDetailView(DetailView):
    template_name = 'author/author_detail.html'
    model = models.Author

class AuthorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'author/author_create.html'
    model = models.Author
    success_url = reverse_lazy('author_list')
    success_message = "Author was created successfully."
    form_class = AuthorForm

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

class BookFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Book
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('book_form_confirmation')
    success_message = "Book was created successfully."
    form_class = BookForm

class BookFormConfirmationView(TemplateView):
    template_name = 'book/book_form_confirmation.html'

class PublisherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'publisher/publisher_create.html'
    model = models.Publisher
    success_url = reverse_lazy('publisher_create')
    success_message = "Publisher was created successfully."
    form_class = PublisherForm

class CatalogueView(ListView):
    template_name = 'catalogue/catalogue.html'
    model = models.Book

class LibraryRulesView(TemplateView):
    template_name = 'for_readers/library_rules.html'

class FAQView(TemplateView):
    template_name = 'for_readers/faq.html'

class RegisterView(CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')
    form_class = RegisterUserForm

class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'my_account/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['library_card'] = {
            'full_name': self.request.user.first_name + ' ' + self.request.user.last_name,
            'membership_ends': self.request.user.reader.membership_end_date,
            'card_number': ' '.join(self.request.user.reader.library_card_number)
        }

        num_of_loans = models.BookLoan.objects.filter(reader=self.request.user.reader, returned_at__isnull=True).count()
        context['num_of_loans'] = num_of_loans

        num_of_reservations = models.BookReservation.objects.filter(reader=self.request.user.reader, termination_type__isnull=True).count()
        context['num_of_reservations'] = num_of_reservations

        return context

class MyLoanView(LoginRequiredMixin, SingleTableView):
    template_name = 'my_account/book_loans.html'
    model = models.BookLoan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_loan = models.BookLoan.objects.filter(reader=self.request.user.reader, returned_at__isnull=True)
        context['book_loan'] = book_loan

        return context

    table_class = tables.MyBookLoanTable

class MyReservationView(LoginRequiredMixin, SingleTableView):
    template_name = 'my_account/reservations.html'
    model = models.BookReservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_reservation = models.BookReservation.objects.filter(reader=self.request.user.reader, termination_type__isnull=True)
        context['book_reservation'] = book_reservation

        return context

    table_class = tables.MyBookReservationTable

class OpenReservationListView(LoginRequiredMixin, SingleTableView):
    model = models.BookReservation
    table_class = tables.OpenReservationTable
    template_name = 'book_reservation/open_reservation_list.html'

    def get_table_data(self):
        return models.BookReservation.objects.filter(termination_type__isnull=True).order_by('-book_available_at', 'created_at')


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

class CompleteBookReservationView(View):

    def post(self, request, *args, **kwargs):

        pk_reservation = self.kwargs['pk']
        reservation = models.BookReservation.objects.get(pk=pk_reservation)
        reservation.termination_type = 'Completed'
        reservation.save()

        messages.success(request, 'Reservation was successfully completed and the book loan created.')
        return HttpResponseRedirect(reverse_lazy('open_reservation_list'))

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

# ------------------------------
#       CUSTOM ERROR PAGE
# ------------------------------

# should later be extended to a class
def custom_error_404(request, exception):
    return render(request, 'errors/404.html', {})

def custom_error_500(request):
    return render(request, 'errors/500.html', {})

def custom_error_403(request, exception):
    return render(request, 'errors/403.html', {})

def custom_error_400(request, exception):
    return render(request, 'errors/400.html', {})