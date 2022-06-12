from django.contrib import admin
import ils.models as models

class BookReservationAdmin(admin.ModelAdmin):
    fields = ['reader', 'book', 'book_available_at', 'termination_type', 'created_at']
    readonly_fields = ['created_at']
    list_display = ['reader', 'book', 'termination_type', 'created_at']
    list_filter = [['termination_type', admin.EmptyFieldListFilter], 'termination_type']
    search_fields = ['reader__user__last_name', 'book__name', 'book__author__first_name', 'book__author__last_name']

class BookAdmin(admin.ModelAdmin):
    fields = ['name', 'author', 'publisher', 'year', 'status', 'description']
    list_display = ['name', 'author', 'status', 'publisher']
    list_filter = ['status']
    search_fields = ['name', 'author__first_name', 'author__last_name', 'description']

class BookLoanAdmin(admin.ModelAdmin):
    fields = ['reader', 'book', 'created_at', 'returned_at']
    readonly_fields = ['created_at']
    list_display = ['reader', 'book', 'created_at', 'returned_at']
    list_filter = ['reader', 'book__author']
    search_fields = ['reader', 'book__name', 'book__author__first_name', 'book__author__last_name']

admin.site.register(models.Author)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookLoan, BookLoanAdmin)
admin.site.register(models.BookReservation, BookReservationAdmin)
admin.site.register(models.Librarian)
admin.site.register(models.Publisher)
admin.site.register(models.Reader)
