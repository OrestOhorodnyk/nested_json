import argparse
import json
import sys
from collections import defaultdict
from typing import List


class DynamicNestedDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DynamicNestedDict, self).__init__(DynamicNestedDict, *args, **kwargs)

    def __default_to_regular(self, d):
        if isinstance(d, DynamicNestedDict):
            d = {k: self.__default_to_regular(v) for k, v in d.items()}
        return d

    def set_from_list(self, keylist, value):
        level = self
        for key in keylist[:-1]:
            level = level[key]
        level[keylist[-1]] = value

    def get_from_list(self, keylist):
        level = self
        for key in keylist[:-1]:
            level = dict(level)
            level = level[key]
        return level[keylist[-1]]

    def to_regular_dict(self):
        return {k: self.__default_to_regular(v) for k, v in self.items()}


def parse_args():
    """
    Parses arguments given application on startup
    :return:tuple of two elements, first element list of keys and second dict to nest
    """
    parser = argparse.ArgumentParser(prog='nest', usage="'cat file.json | python nest.py key1 key2 key3 ... keyN'")

    parser.add_argument('keylist', nargs='+', help='Keys separated by whitespace')
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='JSON to process.')
    args = parser.parse_args()

    if not sys.stdin.isatty():
        input_file = parser.parse_args().stdin.read().splitlines()
    else:
        input_file = []
    input_json = json.loads(''.join(input_file))
    return args.keylist, input_json


def nest(input_dict: List[dict], keys: List[str]) -> List[dict]:
    result = dict()
    dd = DynamicNestedDict()
    try:
        for i in input_dict:
            nested_keys = [i.pop(w) for w in keys]
            dd.set_from_list(nested_keys, [i])
            result.update(dd.to_regular_dict())
    except IndexError:
        raise ValueError(f'Empty keylist {keys}')
    except KeyError as e:
        raise ValueError(f'Key {e.args[0]} not present in the input JSON')
    return result


if __name__ == '__main__':
    args = parse_args()
    keys = args[0]
    input_dict = args[1]
    nested = nest(input_dict=input_dict, keys=keys)
    print(nested)
