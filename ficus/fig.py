import funcy as f
import yaml


class Fig(dict):
    def __str__(self):
        return yaml.dump(to_dict(self))



class FigGroup(Fig):
    # TODO
    pass


class Ficus(list):
    pass
