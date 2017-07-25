# -*- coding: utf-8 -*-
# @Author: wujiyu115
# @Date:   2016-06-08 11:56:39
# @Last Modified by:   far
# @Last Modified time: 2017-07-25 09:28:51

import inspect


def cls_attr_values(cls, filter_attrs=[]):
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    return [a for a in attributes if not a[0].startswith('__') and not a[0].endswith('__') and not a[0] in filter_attrs]


def cls_attrs(cls, filter_attrs=[]):
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    return [a[0] for a in attributes if not a[0].startswith('__') and not a[0].endswith('__') and not a[0] in filter_attrs]


# obj or cls to dict
def obj_dict(obj, filter_attrs=[]):
    return dict((key_value[0], key_value[1]) for key_value in cls_attr_values(obj, filter_attrs))


# dict to obj
def dict_obj(d):
    seqs = tuple, list, set, frozenset
    if isinstance(d, seqs):
        return d
    return warp_dict_obj(d)


def warp_dict_obj(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, warp_dict_obj(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(warp_dict_obj(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top
