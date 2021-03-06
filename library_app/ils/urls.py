from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # For Search results
    # path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('search/', views.search_results, name='search_results'),

    # Author
    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    
    # Book
    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/book_form', views.BookFormView.as_view(), name='book_form'),
    path('book/book_form_confirmation', views.BookFormConfirmationView.as_view(), name='book_form_confirmation'),
    path('book/<int:pk>/reserve/', views.MakeReservationView.as_view(), name='book_make_reservation'),

    # Publisher
    path('publisher/create/', views.PublisherCreateView.as_view(), name='publisher_create'),

    # Catalogue
    path('catalogue/', views.CatalogueView.as_view(), name='catalogue'),

    # For Users
    path('readers/library_rules', views.LibraryRulesView.as_view(), name='library_rules'),
    path('readers/faq', views.FAQView.as_view(), name='faq'),

    # For Registration
    path('register', views.RegisterView.as_view(), name='register'),

    # My Account
    path('my_account', views.MyAccountView.as_view(), name='my_account'),
    path('my_account/book_loans', views.MyLoanView.as_view(), name='account_book_loans'),
    path('my_account/reservations', views.MyReservationView.as_view(), name='account_reservations'),
  
    # Librarian Actions
    path('open_reservations', views.OpenReservationListView.as_view(), name='open_reservation_list'),
    path('open_reservations/<int:pk>/complete/', views.CompleteBookReservationView.as_view(), name='complete_open_reservation'),
    path('open_loans', views.OpenLoanListView.as_view(), name='open_loan_list'),
    path('open_loans/<int:pk>/complete/', views.CompleteBookLoanView.as_view(), name='complete_open_loan'),
]