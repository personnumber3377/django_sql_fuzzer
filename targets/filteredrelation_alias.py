from django.db.models import FilteredRelation, Q, F
from django.core.exceptions import FieldError
from django.db.utils import OperationalError
from django_sql_fuzzer.app.models import Author

def filteredrelation_alias(payload: str):
    """
    Fuzz the alias name of FilteredRelation. Past CVEs allowed SQL injection
    when alias names weren't sanitized.
    """
    try:
        qs = Author.objects.annotate(
            **{
                payload: FilteredRelation(
                    "book",
                    condition=Q(book__rating=F(payload))
                )
            }
        )
        list(qs)
    except (FieldError, OperationalError, ValueError, TypeError):
        return
