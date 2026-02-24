# fuzzer/targets/filtered_relation_alias.py
from django.db.models import FilteredRelation, Q, F
from app.models import Author
from app.models import Book

def filtered_relation_new(payload: str):
    qs = Book.objects.annotate(
        **{payload: FilteredRelation("author")}
    ).order_by(payload)
    # print("Here is the query: "+str(str(qs.query)))
    list(qs)
    return str(qs.query)

