from dynamic_nested_dict import DynamicNestedDict
import pytest


def test_set_from_list():
    levels = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5']

    dd = DynamicNestedDict()
    dd.set_from_list(levels, value=100)

    assert dd['level_1']['level_2']['level_3']['level_4']['level_5'] == 100


def test_set_from_list_empty_list():
    levels = []
    dd = DynamicNestedDict()
    with pytest.raises(IndexError):
        dd.set_from_list(levels, value=100)


def test_to_regular_dict():
    levels = ['level_1', 'level_2']

    dd = DynamicNestedDict()
    dd.set_from_list(levels, value=100)
    regular_dict = dd.to_regular_dict()
    assert regular_dict['level_1']['level_2'] == 100
    assert not isinstance(regular_dict, DynamicNestedDict) and isinstance(regular_dict, dict)
    assert not isinstance(regular_dict['level_1'], DynamicNestedDict) and isinstance(regular_dict['level_1'], dict)
    assert isinstance(regular_dict['level_1']['level_2'], int)
    assert isinstance(dd, DynamicNestedDict)
