# fuzzer/targets/registry.py
from .queryset_alias import qs_alias
from .queryset_json import qs_json_value, qs_json_valuelist
from .queryset_extra import qs_extra
from .queryset_alias_api import qs_alias_api
from .filtered_relation_alias import filteredrelation_alias
from .q_connector import q_connector

TARGETS = [
    qs_alias,
    qs_json_value,
    qs_json_valuelist,
    qs_extra,
    qs_alias_api,
    filteredrelation_alias,
    q_connector,
]
