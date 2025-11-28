from django.db.models.functions import Trunc
from app.models import DTModel

def trunc_function(payload: str):
    try:
        DTModel.objects.filter(
            start_datetime__date=Trunc("start_datetime", payload)
        ).exists()
    except Exception:
        return

