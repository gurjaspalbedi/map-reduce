# -*- coding: utf-8 -*-


def word_count_reducer(reducer_list):
    py_counter = {}
    for tup in reducer_list:
        py_counter[tup.key] = py_counter.get(tup.key,0) +  1
    return py_counter