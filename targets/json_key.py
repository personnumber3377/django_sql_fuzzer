from django.db.utils import OperationalError, ProgrammingError
from app.models import JSONFieldModel
from django.db.models import F
from django.core.exceptions import FieldError

def json_key(payload: str):
    """
    Fuzz JSON key lookups: data__<payload>
    """
    # Equivalent of: SELECT data->payload
    qs = JSONFieldModel.objects.annotate(
        val=F(f"data__{payload}")
    )
    try:
        list(qs)
        # print("query: "+str(str(qs.query)))
        return str(qs.query)
    except (OperationalError, ProgrammingError, ValueError, TypeError, FieldError):
        return str(qs.query)
