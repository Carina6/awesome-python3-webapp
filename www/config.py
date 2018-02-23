#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
'''
import logging
import os

import config_default
from rootdir import root_dir


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)


def logger_config():
    # logging.basicConfig(level=logging.INFO)  设置此配置，会在控制台打印重复log
    Logger = logging.getLogger('')
    Logger.setLevel(logging.INFO)

    LOG_FORMAT = '%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s: %(message)s'

    # config stream log
    console = logging.StreamHandler()
    console.setFormatter(fmt=logging.Formatter(LOG_FORMAT))
    Logger.addHandler(console)

    # config file log

    file = logging.FileHandler(filename=os.path.join(root_dir, 'awesome.log'), mode='w', encoding='utf-8')
    file.setFormatter(fmt=logging.Formatter(LOG_FORMAT))
    Logger.addHandler(file)
