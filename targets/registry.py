from targets.filteredrelation_alias import filteredrelation_alias
from targets.q_connector import q_connector
from targets.queryset_alias_api import qs_alias_api
from targets.queryset_annotate import qs_annotate
from targets.queryset_aggregate import qs_agg
from targets.json_object import json_object
from targets.extract_function import extract_function
from targets.trunc_function import trunc_function
from targets.concat import concat_test

TARGETS = [
    filteredrelation_alias,
    q_connector,
    qs_alias_api,
    qs_annotate,
    qs_agg,
    json_object,
    extract_function,
    trunc_function,
    concat_test,
]