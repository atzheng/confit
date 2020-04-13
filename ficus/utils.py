import funcy as f
from .decorators import figgify


@figgify
def flatten_dict(dkt):
    return dict(f.mapcat(flatten_item, dkt.items()))


@figgify
def flatten_item(it):
    k, v = it
    if isinstance(v, list):
        return [("%s.%d" % (k, i), v[i]) for i in range(len(v))]
    elif isinstance(v, dict):
        return [(k + "." + vk, vv) for (vk, vv) in flatten_dict(v).items()]
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
