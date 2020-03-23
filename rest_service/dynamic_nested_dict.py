from collections import defaultdict


class DynamicNestedDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DynamicNestedDict, self).__init__(DynamicNestedDict, *args, **kwargs)

    def __default_to_regular(self, d):
        if isinstance(d, DynamicNestedDict):
            d = {k: self.__default_to_regular(v) for k, v in d.items()}
        return d

    def to_regular_dict(self):
        return {k: self.__default_to_regular(v) for k, v in self.items()}

    def set_from_list(self, keylist, value):
        level = self
        for key in keylist[:-1]:
            level = level[key]
        level[keylist[-1]] = value
