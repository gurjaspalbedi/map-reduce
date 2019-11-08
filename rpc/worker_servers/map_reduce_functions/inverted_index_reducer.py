# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

def reduce_func(reducer_list):
    py_counter = {}
    for tup in reducer_list:
        key = tup.key
        value_list = tup.value
        
        py_counter[key] = py_counter.get(key,[]) +  value_list
    return py_counter