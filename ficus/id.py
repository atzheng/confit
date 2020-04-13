import hashlib
import json
import re

import funcy as f
from codenamize import codenamize


def str2dict(d):
    return json.dumps(d, sort_keys=True, default=str)


def hash_id(length=6):
    def id(d):
        return hashlib.md5(str2dict(d).encode()).hexdigest()[:length]
    return id


def abbrev_id(fields, length=3):
    fields = [x if isinstance(x, list) else [x] for x in fields]

    def id(d):
        return "_".join(["{fld}={val}".format(
            fld=abbrev(field[-1], length=length),
            val=f.get_in(d, field))
                         for field in fields])
    return id


def codename_id(**kwargs):
    "Human readable hashes."
    def id(d):
        return codenamize(str2dict(d), **kwargs)
    return id


def abbrev(x, length=3):
    # TODO should remove vowels until it achieves length
    if len(x) < length:
        return x
    x = re.sub(r"[^\w\s]", "", x)
    x = x[0] + re.sub(r"[aeiouAEIOU]", "", x[1:])
    return x[:min(length, len(x))]


def cat(*fns, catter="_".join):
    """
    For fns with the same args, apply each fn and concatenate outputs.
    Default assumes each fn returns a str, and concats the strs.
    """
    return f.compose(catter, f.juxt(*fns))
