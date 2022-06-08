from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

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

    # Catalogue
    path('catalogue/', views.CatalogueView.as_view(), name='catalogue'),

    # For Users
    path('readers/library_rules', views.LibraryRulesView.as_view(), name='library_rules'),
    path('readers/faq', views.FAQView.as_view(), name='faq'),

    # For Registration
    path('register', views.RegisterView.as_view(), name='register'),

    # My Account
    path('my_account', views.MyAccountView.as_view(), name='my_account')
]