# -*- coding: utf-8 -*-
import hashlib
import hmac
import time
import urllib
import urllib2
import json
from datetime import datetime
from uuid import UUID
from objutil import dict_obj
# import requests


def http_get(url, data_wrap, encode=False):
    if encode is True:
        data_wrap = urllib.urlencode(data_wrap)
    req = urllib2.Request(url, data=data_wrap)
    resp = urllib2.urlopen(req).read()
    dic = json.loads(resp)
    return dict_obj(dic)


def get_signature(private_key, data):
    data_en = urllib.urlencode(data)
    md5_hash = getHash(private_key)
    msg = bytes(data_en).encode('utf-8')
    key = bytes(md5_hash).encode('utf-8')
    signature = hmac.new(key, msg, digestmod=hashlib.sha256).digest()
    last_warp = "%s&signature=%s" % (data_en, toHex(signature))
    return last_warp


def get_nonce_time():
    curr_stamp = time.time() * 100
    return str(long(curr_stamp))


def getHash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def toHex(str):
    lst = []
    for ch in str:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0' + hv
        lst.append(hv)
    return reduce(lambda x, y: x + y, lst)


def getUserData(cfg_file):
    f = open(cfg_file, 'r')
    account = {}
    for i in f.readlines():
        ctype, passwd = i.split('=')
        account[ctype.strip()] = passwd.strip()

    return account


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(result):
    return json.dumps(result, cls=CJsonEncoder)
