# -*- coding: utf-8 -*-
from uuid import uuid3, NAMESPACE_DNS


def req_m(req):
    if (req.method == "POST"):
        return 1
    if (req.method == "GET"):
        return 0
    if (req.method == "PUT"):
        return 2
    if (req.method == "DELETE"):
        return 3


def search_url(req_m):
    return req_m.args.get("q", type=str, default=None)


def create_uuid(name):
    return str(uuid3(NAMESPACE_DNS, name=name))


def test_print(values):
    print("===================\n")
    print(values)
    print("\n===================")
