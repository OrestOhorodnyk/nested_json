from nest import nest
import pytest


def test_nest_3_keys():
    input_dict = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]
    keys = ['currency', 'country', 'city']
    expected_result = {
        "EUR": {
            "ES": {
                "Madrid": [
                    {
                        "amount": 8.9
                    }
                ]
            },
            "FR": {
                "Lyon": [
                    {
                        "amount": 11.4
                    }
                ],
                "Paris": [
                    {
                        "amount": 20
                    }
                ]
            }
        },
        "FBP": {
            "UK": {
                "London": [
                    {
                        "amount": 10.9
                    }
                ]
            }
        },
        "GBP": {
            "UK": {
                "London": [
                    {
                        "amount": 12.2
                    }
                ]
            }
        },
        "USD": {
            "US": {
                "Boston": [
                    {
                        "amount": 100
                    }
                ]
            }
        }
    }

    result = nest(input_dict, keys)

    assert result == expected_result


def test_nest_4_keys():
    input_dict = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100,
            "client_id": "1"
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20,
            "client_id": "31"
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4,
            "client_id": "11"
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9,
            "client_id": "2"
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2,
            "client_id": "2"
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9,
            "client_id": "1"
        }
    ]
    keys = ['client_id', 'currency', 'country', 'city']
    expected_result = {
        '1': {'USD': {'US': {'Boston': [{'amount': 100}]}}, 'FBP': {'UK': {'London': [{'amount': 10.9}]}}},
        '31': {'EUR': {'FR': {'Paris': [{'amount': 20}]}}}, '11': {'EUR': {'FR': {'Lyon': [{'amount': 11.4}]}}},
        '2': {'EUR': {'ES': {'Madrid': [{'amount': 8.9}]}}, 'GBP': {'UK': {'London': [{'amount': 12.2}]}}}}

    result = nest(input_dict, keys)

    assert result == expected_result


def test_nest_no_keys():
    input_dict = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]
    keys = []
    with pytest.raises(ValueError) as e:
        nest(input_dict, keys)

    assert e.value.args[0] == f'Empty keylist {keys}'


def test_nest_wrong_keys():
    input_dict = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]
    keys = ['wrong key1', 'wrong key2']
    with pytest.raises(ValueError) as e:
        nest(input_dict, keys)

    assert e.value.args[0] == f'Key {keys[0]} not present in the input JSON'


def test_nest_empty_input_dict():
    input_dict = []
    keys = ['wrong key1', 'wrong key2']
    result = nest(input_dict, keys)
    assert result == {}


input_dict = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100,
        "client_id": "1"
    },
    {
        "country": "FR",
        "city": "Paris",
        "currency": "EUR",
        "amount": 20,
        "client_id": "31"
    },
    {
        "country": "FR",
        "city": "Lyon",
        "currency": "EUR",
        "amount": 11.4,
        "client_id": "11"
    },
    {
        "country": "ES",
        "city": "Madrid",
        "currency": "EUR",
        "amount": 8.9,
        "client_id": "2"
    },
    {
        "country": "UK",
        "city": "London",
        "currency": "GBP",
        "amount": 12.2,
        "client_id": "2"
    },
    {
        "country": "UK",
        "city": "London",
        "currency": "FBP",
        "amount": 10.9,
        "client_id": "1"
    }
]


def test_nest_4_keys():
    input_dict = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100,
            "client_id": "1"
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20,
            "client_id": "31"
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4,
            "client_id": "11"
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9,
            "client_id": "2"
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2,
            "client_id": "2"
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9,
            "client_id": "1"
        }
    ]
    keys = ['client_id', 'currency', 'country', 'city']
    expected_result = {
        '1': {'USD': {'US': {'Boston': [{'amount': 100}]}}, 'FBP': {'UK': {'London': [{'amount': 10.9}]}}},
        '31': {'EUR': {'FR': {'Paris': [{'amount': 20}]}}}, '11': {'EUR': {'FR': {'Lyon': [{'amount': 11.4}]}}},
        '2': {'EUR': {'ES': {'Madrid': [{'amount': 8.9}]}}, 'GBP': {'UK': {'London': [{'amount': 12.2}]}}}}

    result = nest(input_dict, keys)

    assert result == expected_result
