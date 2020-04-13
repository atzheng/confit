import os
import itertools as it
import json
import pickle as pkl

import funcy as f
import pandas as pd
import yaml

from .id import codename_id
from .decorators import figgify, vectorize
from .utils import recursive_merge, flatten_dict, set_in_fn


# Additional config utilities
# -------------------------------------------------------------------------
# All of these functions accept a list or Ficus and returns an object of
# the same type.
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
    return vectorize(set_in_fn)(cfgs, [key], id_fn)


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
    get_manifest(cfgs).to_csv(os.path.join(root, "manifest.csv"), index=False)


def get_manifest(cfgs):
    flat_configs = list(map(flatten_dict, cfgs))
    df = pd.DataFrame.from_dict(flat_configs)
    return df
