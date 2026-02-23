from targets.filteredrelation_alias import filteredrelation_alias
from targets.q_connector import q_connector
from targets.queryset_alias_api import qs_alias_api
from targets.queryset_annotate import qs_annotate
from targets.queryset_aggregate import qs_agg
from targets.json_object import json_object
from targets.extract_function import extract_function
from targets.trunc_function import trunc_function
from targets.concat import concat_test

from targets.json_key import json_key
from targets.window import window
from targets.extra import extra
from targets.order_by import order_by
from targets.complex_annotation import complex_annotation

# Newest stuff here
from targets.filtered_relation_new import filtered_relation_new

'''
-rw-r--r-- 1 oof oof  473 Nov 28 20:08 json_key.py
-rw-r--r-- 1 oof oof  594 Nov 28 20:07 window.py
-rw-r--r-- 1 oof oof  512 Nov 28 20:07 extra.py
-rw-r--r-- 1 oof oof  443 Nov 28 20:07 order_by.py
'''

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
    json_key,
    window,
    # extra,
    # order_by,
    complex_annotation,
    filtered_relation_new, # This is for the newest SQL injection bug... Use this one please...
]
