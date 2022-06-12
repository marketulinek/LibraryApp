import django_tables2 as tables
from ils.models import BookLoan
from django_tables2.utils import A

class MyBookLoanTable(tables.Table):
    class Meta:
        model = BookLoan
        fields = ("book__name", "book__author", "created_at", "returned_at")

    book__name = tables.LinkColumn("book_detail", args=[A("pk")],
                                attrs={"a": {"class": "cell-with-link"}})
