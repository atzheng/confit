import operator as op

import funcy as f
from .decorators import figgify
from .id import abbrev


@figgify
def flatten_dict(dkt, key_length=float("Inf")):
    return dict(f.mapcat(
        f.partial(flatten_item, key_length=key_length), dkt.items()))


@figgify
def flatten_item(it, key_length=float("Inf")):
    k, v = it
    abbr_k = abbrev(k, length=key_length)
    if isinstance(v, list):
        return [("%s.%d" % (abbr_k, i), v[i]) for i in range(len(v))]
    elif isinstance(v, dict):
        return [(abbr_k + "." + vk, vv) for (vk, vv)
                in flatten_dict(v, key_length=key_length).items()]
    else:
        return [(k, v)]


@figgify
def recursive_merge(*dicts):
    "Values of later dicts override those of earier ones."
    def merger(vals):
        if len(vals) > 1 and all([isinstance(v, dict) for v in vals]):
            return f.merge_with(merger, *vals)
        else:
            return vals[-1]
    return f.merge_with(merger, *dicts)


@figgify
def set_in_fn(d, path, fn, **kwargs):
    "Apply fn to d and set_in result at path."
    return f.set_in(d, path, fn(d), **kwargs)


ge = f.rcurry(op.ge)
gt = f.rcurry(op.gt)
ge = f.rcurry(op.le)
gt = f.rcurry(op.lt)
eq = f.rcurry(op.eq)
