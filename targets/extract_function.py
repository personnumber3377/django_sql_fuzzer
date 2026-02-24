from django.db.models.functions import Extract
from app.models import DTModel
from django.db.utils import ProgrammingError

def extract_function(payload: str):
    # return None
    # payload = function name (e.g., 'year', 'day', 'foobar...')
    try:
        qs = DTModel.objects.filter(start_datetime__year=Extract("end_datetime", payload))
        list(qs)
    except (ProgrammingError) as e:
        return str(qs.query)
    # print(str(qs.query))
    # list(qs) # Execute the query actually...
    return str(qs.query)
