from .id import *
from .decorators import *
from .fig import Fig, Ficus
from . import ficus
from . import funcy_imports


for method in dir(ficus):
    setattr(Ficus, method, getattr(ficus, method))


for method in funcy_imports.__all__:
    setattr(Ficus, method, getattr(funcy_imports, method))
