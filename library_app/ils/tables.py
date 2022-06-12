import django_tables2 as tables
from ils.models import BookReservation
from django_tables2.utils import A

class MyBookReservationTable(tables.Table):
    class Meta:
        model = BookReservation
        fields = ("book__name", "book__author", "created_at", "book_available_at", "termination_type")

    book__name = tables.LinkColumn("book_detail", args=[A("pk")],
                                attrs={"a": {"class": "cell-with-link"}})