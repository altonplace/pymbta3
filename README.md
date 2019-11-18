# pymbta3
Python wrapper for the MBTA v3 API

## Install

pip install pymbta3

## Usage

To get data from the MBTA API, import the library and call the object with your API key. The API Key may also be stored in the environment variable ``MBTA_API_KEY``.

```python
from pymbta3.alerts import Alerts

at = Alerts(key=YOUR_API_KEY_HERE)

# Find all alerts affecting the Red Line at Alewife
alerts = at.get_alert(route='Red', stop='place-alfcl')

# Find the short header for the alert
for alert in alerts['data']:
    print(alert['attributes']['short_header'])
```

Multiple values can be passed in for most lists.

```python
# Alerts affecting Orange and Red lines
alerts = at.get_alert(route=['Orange', 'Red'])
```

```python
# find all alerts affecting parking or Wheelchair use
alerts = at.get_alert(activity=['PARK_CAR', 'USING_WHEELCHAIR'])
```
