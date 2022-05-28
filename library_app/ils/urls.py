from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

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

    # For Users
    path('readers/library_rules', views.LibraryRulesView.as_view(), name='library_rules'),
    path('readers/faq', views.FAQView.as_view(), name='faq')
]