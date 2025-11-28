# fuzzer/targets/queryset_json.py
from app.models import JSONFieldModel

def qs_json_value(payload):
    list(JSONFieldModel.objects.values(f"data__{payload}"))

def qs_json_valuelist(payload):
    list(JSONFieldModel.objects.values_list(f"data__{payload}"))
