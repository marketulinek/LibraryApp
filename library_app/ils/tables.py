import django_tables2 as tables
from django_tables2.utils import A
from ils.models import BookLoan
from ils.models import BookReservation

class MyBookLoanTable(tables.Table):
    created_at = tables.DateTimeColumn(format='D d M Y')
    returned_at = tables.DateTimeColumn(format='D d M Y')

    class Meta:
        model = BookLoan
        fields = ("book__name", "book__author", "created_at", "returned_at")

    book__name = tables.LinkColumn("book_detail", args=[A("pk")],
                                attrs={"a": {"class": "cell-with-link"}})

class MyBookReservationTable(tables.Table):
    created_at = tables.DateTimeColumn(format='D d M Y')
    book_available_at = tables.DateTimeColumn(format='D d M Y')

    class Meta:
        model = BookReservation
        fields = ("book__name", "book__author", "created_at", "book_available_at", "termination_type")

    book__name = tables.LinkColumn("book_detail", args=[A("pk")],
                                attrs={"a": {"class": "cell-with-link"}})

class OpenReservationTable(tables.Table):
    id = tables.Column(verbose_name='#')
    book = tables.Column(verbose_name='Book (author)')
    book_available_at = tables.DateTimeColumn(format='D d M Y')

    class Meta:
        model = BookReservation
        fields = ('id', 'reader', 'book', 'book_available_at')
    
    actions = tables.TemplateColumn(template_name='book_reservation/open_reservation_list_action_column.html', orderable=False)


class OpenLoanTable(tables.Table):
    id = tables.Column(verbose_name='#')
    book = tables.Column(verbose_name='Book (author)')
    created_at = tables.DateTimeColumn(format='D d M Y')

    class Meta:
        model = BookLoan
        fields = ('id', 'reader', 'book', 'created_at')

    actions = tables.TemplateColumn(template_name='book_loan/open_loan_list_action_column.html',
                                    orderable=False)