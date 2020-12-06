# pymbta3
Python wrapper for the MBTA v3 API

## Install

pip install pymbta3

## Usage

To get data from the MBTA API, import the library and call the object with your API key. The API Key may also be stored in the environment variable ``MBTA_API_KEY``.

```python
from pymbta3 import Alerts

at = Alerts(key=YOUR_API_KEY_HERE)

# Find all alerts affecting Alewife
alerts = at.get(stop='place-alfcl')

# Find the short header for the alert
for alert in alerts['data']:
    print(alert['attributes']['short_header'])
```

### Multiple values can be passed in for most filters.

Alerts affecting Orange and Red lines
```python
alerts = at.get(route=['Orange', 'Red'])
```

Alerts affecting parking or Wheelchair use
```python
alerts = at.get(activity=['PARK_CAR', 'USING_WHEELCHAIR'])
```

### Include other data
Return the stop data along with routes
```python
from pymbta3 import Routes

rt = Routes(key=YOUR_API_KEY_HERE)

# Find all Route data for the Red Line
routes = rt.get(route='Red', include='stops')

```
### API Methods Implented

- Alerts
- Routes
- Stops
- Vehicles

