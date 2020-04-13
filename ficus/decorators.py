import funcy as f
from .fig import Fig, Ficus


def swap(fn):
    "Swaps the first and second arguments of fn."
    @f.wraps(fn)
    def swapped(*args, **kwargs):
        head, tail = f.lsplit_at(2, args)
        return fn(*reversed(head), *tail, **kwargs)
    return swapped


def vectorize(fn):
    """
    For fn: list => list, add a kwarg pred, and apply fn
    to the subset of its first arg satisfying pred, leaving
    the complement untouched.
    """
    @f.wraps(fn)
    def vectorized(*args, pred=f.constantly(True), **kwargs):
        return [fn(arg, *f.rest(args), **kwargs)
                if pred(arg) else arg
                for arg in f.first(args)]
    return vectorized


def figgify(fn):
    "Wraps output in a Ficus object if input is a Ficus object."
    @f.wraps(fn)
    def figgified(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(args[0], Fig) or isinstance(args[0], Ficus):
            return to_ficus(result)
        else:
            return result
    return figgified


def to_ficus(x):
    if f.is_seq(x):
        return Ficus(x)
    if f.is_mapping(x):
        return Fig(x)
    else:
        return x
