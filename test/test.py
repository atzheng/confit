import ficus as f


def test_imports():
    cfg = f.Ficus([dict(a=1, b=2), dict(a=1, c=3)])
    assert cfg.omit("a") == f.Ficus([dict(b=2), dict(c=3)])
    assert cfg.pluck("a") == [1, 1]
    assert (cfg.walk_values(lambda x: x + 1) ==
            f.Ficus([dict(a=2, b=3), dict(a=2, c=4)]))


def test_decorators():
    fs = f.swap(lambda a, b: a - b)
    fv = f.vectorize(fs)
    ff = f.figgify(fv)
    assert fs(1, 2) == 1
    assert fv([2, 3, 4], 5) == [3, 2, 1]
    assert fv([2, 3, 4], 5, pred=lambda x: x > 2) == [2, 2, 1]
    assert not isinstance(ff([2, 3, 4], 5), f.Ficus)
    assert isinstance(ff(f.Ficus([2, 3, 4]), 5), f.Ficus)


def test_ids():
    d = dict(Aefg_w0=1, b=dict(c=2))
    fields = ["Aefg_w0", ["b", "c"]]
    abbrev = f.abbrev_id(fields)
    id_fn = f.cat(abbrev, f.hash_id(6))
    assert abbrev(d) == "Afg=1_c=2"
    assert id_fn(d) == "Afg=1_c=2_fea656"
