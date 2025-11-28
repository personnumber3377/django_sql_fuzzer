# fuzzer/targets/registry.py
from targets.queryset_alias import qs_alias
from targets.queryset_json import qs_json_value, qs_json_valuelist
from targets.queryset_extra import qs_extra
from targets.queryset_alias_api import qs_alias_api
from targets.filtered_relation_alias import filteredrelation_alias
from targets.q_connector import q_connector

TARGETS = [
    qs_alias,
    qs_json_value,
    qs_json_valuelist,
    # qs_extra,
    qs_alias_api,
    filteredrelation_alias,
    q_connector,
]
