from django.db.models.functions import Extract
from app.models import DTModel

def extract_function(payload: str):
    try:
        # payload = function name (e.g., 'year', 'day', 'foobar...')
        DTModel.objects.filter(start_datetime__year=Extract("end_datetime", payload)).exists()
    except Exception:
        return
