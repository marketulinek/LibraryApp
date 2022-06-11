import django_tables2 as tables
from ils.models import BookReservation


class OpenReservationTable(tables.Table):
    id = tables.Column(verbose_name='#')
    book = tables.Column(verbose_name='Book (author)')
    book_available_at = tables.DateTimeColumn(format='D d M Y')

    class Meta:
        model = BookReservation
        fields = ('id', 'reader', 'book', 'book_available_at')
    
    actions = tables.TemplateColumn(template_name='book_reservation/open_reservation_list_action_column.html', orderable=False)