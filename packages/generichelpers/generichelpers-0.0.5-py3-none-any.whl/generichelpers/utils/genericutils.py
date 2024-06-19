# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:22:32 2020
@author: Ratnadip Adhikari
"""

# ================================================
import json
import time
import re
import pandas as pd
import inspect
from concurrent.futures import ThreadPoolExecutor
from undecorated import undecorated
from datetime import timedelta

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')
# +++++++++++++++++
# Set python options
from IPython.core import display
pd.set_option('display.max_columns', None)
# pd.reset_option('display.max_columns')
# print('python version: ', python_version())
# print('script path: ', os.path.join(os.path.dirname(__file__),''))
# print('sys.version: ', sys.version)
# ================================================


# ==================================
# Decorator to compute elapsed time for any function
# ==================================
"""
## Quick helps on decorated functions
# from undecorated import undecorated ##[for stripping decorator from a function]
%load inspect.getsource(function_name)
# =================
For loading the base function that is decorated
%load inspect.getsource(base_func_name.__closure__[0].cell_contents)
%load inspect.getsource(undecorated(base_func_name))
help(undecorated(base_func_name)) #for console help
# =================
func_2 = base_func_name.__closure__[0].cell_contents
func_2 = undecorated(base_func_name)
"""
def elapsedTime(func):
    """"This is a decorator to compute elapsed time for any function.
    Add arguments inside the ``calcTime()`` func if the target func uses arguments.
    The ``print_el_time`` parameter controls the printing and it should be present in the target
    function. Else, by default elapsed time will be printed after that function call.
    """
    def calcTime(*args, **kwargs):
        # storing time before function execution
        st_time = time.monotonic()
        ret_val = func(*args, **kwargs)
        end_time = time.monotonic()
        el_time = timedelta(seconds=end_time - st_time) # find elapsed time
        argsDict = {k: v for k, v in kwargs.items()}
        if 'print_el_time' in argsDict:
            if argsDict['print_el_time']:
                print('Elapsed time for <{0}> func is: {1}'.format(func.__name__, el_time))
        else:
            print('Elapsed time for <{0}> func is: {1}'.format(func.__name__, el_time))
        return ret_val
    return calcTime


def null_handler(obj, ret_val):
    """Return `ret_val` if 'obj' is `None` or empty"""
    if not obj:
        return ret_val
    return obj


def map_processing(func, args, to_unpack=False):
    """Map lambda processing of multiple calls of a func"""
    res = map(lambda p: func(*p), args) if to_unpack else map(func, args)
    return list(res)


def multi_threading(func, args, workers, to_unpack=False):
    """Multithreading execution of a func"""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(lambda p: func(*p), args) if to_unpack else executor.map(func, args)
    return list(res)


def get_func_attrs(attrs_dict: dict, func_obj, to_strip=True, to_print=True):
    """Returns valid attributes for func: `func_name` from the passed `attrs_dict`. The `func_obj` can
    accept class too in some cases. The param: `to_strip` is for removing decorators from `func_name`."""
    # dict of <func_name> (args, default_vals)
    try:
        func_sign = inspect.signature(undecorated(func_obj)).parameters if to_strip \
            else inspect.signature(func_obj).parameters
        func_attrs = {k: str(v) for k, v in func_sign.items()}
        for k, v in func_attrs.items():
            assign_v = (
                v.replace("{}=".format(k), "").replace("{}: ".format(k), "")
                if any(re.findall(r"=|:", v))
                else "__NON_DEFAULT__"
            )
            try:
                assign_v = eval(assign_v)
            except Exception:
                pass
            func_attrs[k] = assign_v
        # +++++++++++++++++
        if attrs_dict:
            func_attrs = dict(func_sign)
            func_attrs = {k: v for k, v in attrs_dict.items() if k in func_attrs.keys()}
    except Exception:
        func_attrs = {}
    if to_print:
        print(json.dumps(func_attrs, indent=4, default=str))
    return func_attrs


def get_obj_attributes(class_obj, exclude_attrs=[]):
    """Extract custom attributes (not functions or built-in attribute) from a class object"""
    custom_attributes, all_attrs = {}, dir(class_obj)
    for attr_name in all_attrs:
        attr_value = getattr(class_obj, attr_name)
        if not (callable(attr_value) or attr_name.startswith("__") or attr_name in exclude_attrs):
            custom_attributes[attr_name] = attr_value
    return custom_attributes
