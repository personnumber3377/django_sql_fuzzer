from django.db.utils import OperationalError, ProgrammingError
from app.models import JSONFieldModel
from django.db.models import F

def json_key(payload: str):
    """
    Fuzz JSON key lookups: data__<payload>
    """
    try:
        # Equivalent of: SELECT data->payload
        qs = JSONFieldModel.objects.annotate(
            val=F(f"data__{payload}")
        )
        list(qs)
    except (OperationalError, ProgrammingError, ValueError, TypeError):
        return
