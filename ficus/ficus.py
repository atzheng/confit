import os
import itertools as it
import json
import pickle as pkl

import funcy as f
import pandas as pd
import yaml

from .id import codename_id, abbrev
from .decorators import figgify, vectorize
from .utils import recursive_merge, flatten_dict, set_in_fn
from .funcy_imports import project, walk_keys


# Additional config utilities
# -------------------------------------------------------------------------
# All of these functions accept a list or Ficus and returns an object of
# the same type.
set_in_fn = vectorize(set_in_fn)


@figgify
def product(*args, pred=f.constantly(True)):
    """
    Merge all combinations of the elements of args, where
    predicate(el1, el2, ...) is True.
    """
    return [recursive_merge(*ds)
            for ds in it.product(*args) if pred(*ds)]


@figgify
def namespace(cfgs, name):
    return [{name: cfg} for cfg in cfgs]


@figgify
def generate_ids(cfgs, id_fn=codename_id(), key="config_id"):
    return set_in_fn(cfgs, [key], id_fn)


def to_dict(item):
    if f.is_mapping(item):
        return f.walk_values(to_dict, item)
    elif f.is_seq(item):
        return f.lmap(to_dict, item)
    else:
        return item


# Output
# -------------------------------------------------------------------------
def write_configs(cfgs, root=".", format="json",
                  key="config_id", manifest=True):
    writers = dict(json=json.dump, yaml=yaml.dump, pkl=pkl.dump)
    writer = writers[format]
    cfg_ids = [cfg[key] for cfg in cfgs]
    for (id, cfg) in zip(cfg_ids, cfgs):
        path = os.path.join(root, id)
        os.makedirs(path, exist_ok=True)
        fname = os.path.join(path, "config.{ext}".format(ext=format))
        with open(fname, "w") as file:
            writer(cfg, file)


def write_manifest(cfgs, root=".", **kwargs):
    path = os.path.join(root, "manifest.csv")
    get_manifest(cfgs, **kwargs).to_csv(path, index=False)


def get_manifest(cfgs, simplify=True, key_length=float("Inf")):
    flat_configs = f.lmap(
        f.partial(flatten_dict, key_length=key_length), cfgs)
    if simplify:
        valid_keys = [k for k, vs in f.zip_dicts(*flat_configs)
                      if len(f.ldistinct(vs)) > 1]
        flat_configs = project(flat_configs, valid_keys)
    df = pd.DataFrame.from_dict(flat_configs)
    return df
