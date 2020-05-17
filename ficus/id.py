import hashlib
import json

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

    def prefix(fld):
        if length == 0:
            return ""
        else:
            return abbrev(fld[-1], length=length) + "="

    def id(d):
        return "_".join([
            "{pfx}{val}".format(pfx=prefix(field), val=f.get_in(d, field))
            for field in fields])

    return id


def codename_id(**kwargs):
    "Human readable hashes."
    def id(d):
        return codenamize(str2dict(d), **kwargs)
    return id


def abbrev(x, length=3):
    if len(x) <= length:
        return x
    priorities = [1] + f.lmap(priority, f.rest(x))
    idx = sorted(f.lzip(*f.take(length, argsort(priorities)))[1])
    abbr = "".join([x[i] for i in idx])
    return abbr


def priority(c):
    if c in "_.- \t":
        return 5
    elif c in "aeiouAEIOU":
        return 2
    else:
        return 1


def argsort(lst):
    return sorted((e, i) for i, e in enumerate(lst))


def cat(*fns, catter="_".join):
    """
    For fns with the same args, apply each fn and concatenate outputs.
    Default assumes each fn returns a str, and concats the strs.
    """
    return f.compose(catter, f.juxt(*fns))
