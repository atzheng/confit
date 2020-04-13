import funcy as f

from .decorators import figgify, vectorize, swap


_to_vectorize = dict(
    omit=f.omit,
    project=f.project,
    get_in=f.get_in,
    set_in=f.set_in,
    compact=f.compact,
    is_distinct=f.is_distinct,
    update_in=f.update_in)


_to_swap = dict(
    pluck=f.lpluck,
    map=f.lmap,
    filter=f.lfilter)


_to_swap_and_vectorize = dict(
    walk=f.walk,
    walk_values=f.walk_values,
    walk_keys=f.walk_keys,
    select=f.select,
    select_values=f.select_values,
    select_keys=f.select_keys,
    merge_with=f.merge_with)


_to_import = dict(
    where=f.where,
    invoke=f.invoke)


_all = f.merge(
    f.walk_values(f.compose(figgify, vectorize),
                  _to_vectorize),
    f.walk_values(f.compose(figgify, vectorize, swap),
                  _to_swap_and_vectorize),
    f.walk_values(f.compose(figgify, swap), _to_swap),
    f.walk_values(figgify, _to_import))


for (k, v) in _all.items():
    globals()[k] = v


__all__ = list(_all.keys())
