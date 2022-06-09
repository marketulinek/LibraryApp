import django_tables2 as tables
from ils.models import BookReservation


class OpenReservationTable(tables.Table):
    class Meta:
        model = BookReservation
        fields = ('reader', 'book', 'book_available_at')