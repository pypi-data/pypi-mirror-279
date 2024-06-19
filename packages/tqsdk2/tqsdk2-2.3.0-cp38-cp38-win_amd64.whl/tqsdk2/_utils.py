#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chenli'

import uuid


def get_mac_address():
    mac = f"{uuid.getnode():012X}"
    return "-".join([mac[e:e + 2] for e in range(0, 11, 2)])
