***NEST REST SERVISE***

**Required:**
* python 3.7
* pipenv or virtualenv 

**To run the app:**

* navigate to the project directory: `cd rest_service/`

* create env: ```pipenv install```

* activate env: ```pipenv shell```

OR 

* create env: ```virtualenv -p python3.7 venv```

* activate env: ```source venv/bin/activate```

* make sure that port 5000 on your local host is not used

* run app python app.py

**The app will be available by the link** `http://0.0.0.0:5000`

One can use swagger ui to test endpoints, it's available by the link http://localhost:5000/ui

**To make sure that the application app and running**

`curl -X GET "http://localhost:5000/health" -H "accept: */*"`

the response should be `200, {"status": "OK"}`

**Create the nested JSON use `/nested_json` endpoint**

To access this endpoint authentication needed, use this creads: user: admin, password: admin

You should provide key list in query parameters and flat JSON in the request body, both are required.

Example:
```
curl -X POST "http://localhost:5000/nested_json?keys=currency&keys=country&keys=city" -H "accept: application/json"
-H "Authorization: Basic YWRtaW46YWRtaW4=" -H "Content-Type: application/json" 
-d "[{\"country\":\"US\",\"city\":\"Boston\",\"currency\":\"USD\",\"amount\":100},{\"country\":\"FR\",\"city\":
\"Paris\",\"currency\":\"EUR\",\"amount\":20},{\"country\":\"FR\",\"city\":\"Lyon\",\"currency\":\"EUR\",\
"amount\":11.4},{\"country\":\"ES\",\"city\":\"Madrid\",\"currency\":\"EUR\",\"amount\":8.9},
{\"country\":\"UK\",\"city\":\"London\",\"currency\":\"GBP\",\"amount\":12.2},{\"country\":\"UK\",\"city\":\"London\",
\"currency\":\"FBP\",\"amount\":10.9}]"
```

The response will be:

```json
{
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

```  

**To run test**
* navigate to the project directory: `cd rest_service/`
* create and activate environment
* run ``pytest -vv``