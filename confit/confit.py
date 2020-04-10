import os
import json
import pickle as pkl

import funcy as f
import pandas as pd
import itertools as it
import toolz.dicttoolz as dtz
import yaml

import confit.id as cid

# Utilities for manipulating configs (lists of dicts).
# TODO make default factories orderedDict


# Utilities
# -------------------------------------------------------------------------
def flatten_dict(dkt):
    return dict(it.chain(*map(flatten_item, dkt.items())))


def flatten_item(it):
    k, v = it
    if isinstance(v, list):
        return [("%s_%d" % (k, i), v[i]) for i in range(len(v))]
    elif isinstance(v, dict):
        return [(k + "_" + vk, vv) for (vk, vv) in flatten_dict(v).items()]
    else:
        return [(k, v)]


def str2dict(d):
    return json.dumps(d, sort_keys=True)


# Config generation
# -------------------------------------------------------------------------
def filter(cfgs, predicate):
    return list(filter(predicate, cfgs))


def apply(cfgs, fn, *args, predicate=f.constantly(True), **kwargs):
    """
    Apply fn with args and kwargs to the elements of cfgs
    matching predicate, leaving the others alone.
    """
    return [fn(cfg, *args, **kwargs)
            if predicate(cfg) else cfg
            for cfg in cfgs]


def assoc_in_fn(d, keys, fn, **kwargs):
    return dtz.assoc_in(d, keys, fn(d), **kwargs)


def cartesian(A, B):
    return [dtz.merge(a, b) for (a, b) in it.product(A, B)]


# Output
# -------------------------------------------------------------------------
def generate_config_ids(cfgs, id_fn=cid.codename_id()):
    return apply(cfgs, assoc_in_fn, ["config_id"], id_fn)


def write_configs(cfgs, root=".", format="json"):
    writers = dict(json=json.dump, yaml=yaml.dump, pkl=pkl.dump)
    writer = writers[format]

    cfg_ids = [cfg["config_id"] for cfg in cfgs]
    for (id, cfg) in zip(cfg_ids, cfgs):
        path = os.path.join(root, id)
        os.makedirs(path, exist_ok=True)
        fname = os.path.join(path, "config.{ext}".format(ext=format))
        with open(fname, "w") as file:
            writer(cfg, file)


def get_manifest(cfgs):
    flat_configs = list(map(flatten_dict, cfgs))
    return pd.DataFrame.from_dict(flat_configs)

