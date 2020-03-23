def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200


def test_nest_bad_credentials(client, invalid_credentials):
    headers = {"Authorization": f"Basic {invalid_credentials}"}
    response = client.post('/nested_json', headers=headers)
    assert response.status_code == 401


def test_nest(client, valid_credentials):
    headers = {"Authorization": f"Basic {valid_credentials}"}
    url = 'nested_json?keys=currency&keys=country&keys=city'
    body = [
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
    response = client.post(url, headers=headers, json=body)
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
    assert response.status_code == 200
    assert response.json == expected_result


def test_nest_no_keys_param(client, valid_credentials):
    headers = {"Authorization": f"Basic {valid_credentials}"}
    url = 'nested_json'
    body = [
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
    response = client.post(url, headers=headers, json=body)
    assert response.status_code == 400
    assert response.json['detail'] == "Missing query parameter 'keys'"


def test_nest_invalid_key(client, valid_credentials):
    headers = {"Authorization": f"Basic {valid_credentials}"}
    url = 'nested_json?keys=not_in_the_input'
    body = [
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
    response = client.post(url, headers=headers, json=body)
    assert response.status_code == 422
    assert response.json['detail'] == 'Key not_in_the_input not present in the input JSON'
