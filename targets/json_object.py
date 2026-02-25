from django.db.models.functions import JSONObject, Lower
from django.db.models import F, Value
from app.models import Author

def json_object(payload: str):
    qs = Author.objects.annotate(
        obj=JSONObject(
            name=Lower("name"),
            bad_key=payload,
            age=F("age") + 1,
        )
    )
    qs.first()
    return qs.query
