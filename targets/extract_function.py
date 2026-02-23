from django.db.models.functions import Extract
from app.models import DTModel

def extract_function(payload: str):
    # payload = function name (e.g., 'year', 'day', 'foobar...')
    qs = DTModel.objects.filter(start_datetime__year=Extract("end_datetime", payload)).exists()
    return str(qs.query)
