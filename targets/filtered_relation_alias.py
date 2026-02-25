# fuzzer/targets/filtered_relation_alias.py
from django.db.models import FilteredRelation, Q, F
from app.models import Author

def filteredrelation_alias(payload):
    qs = Author.objects.annotate(
        **{payload: FilteredRelation("book", condition=Q(book__rating=F(payload)))}
    )
    list(qs)
    return qs.query
