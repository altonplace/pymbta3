import os
from functools import wraps
import inspect
from typing import Union

import requests


class PyMBTA3(object):
    """
    Base class where the decorators and base function for the other classes of this python wrapper will inherit from.
    """
    _MBTA_V3_API_URL = 'https://api-v3.mbta.com'

    def __init__(self, key: str = None):
        """ Initialize the class
        Keyword Arguments:
            key:  MBTA v3 api key
        """
        if key is None:
            os.getenv('MBTA_API_KEY')
        if not key or not isinstance(key, str):
            raise ValueError('The MBTA-V3 API key must be provided either through the key parameter or '
                             'through the environment variable MBTA_API_KEY. Get a free key '
                             'from the MBTA website: https://api-v3.mbta.com/')

        self.key = key

        self.headers = {"X-API-Key":  self.key, "accept": 'application/vnd.api+json'}

    @classmethod
    def _call_api_on_func(cls, func):
        """
        Decorator for forming the api call with the arguments of the function, it works by taking the arguments
        given to the function and building the url to call the api on it
        Keyword Arguments:
            func:  The function to be decorated
        """
        # Argument Handling
        argspec = inspect.getfullargspec(func)
        try:
            # Assume most of the cases have a mixed between args and named args
            positional_count = len(argspec.args) - len(argspec.defaults)
            defaults = dict(zip(argspec.args[positional_count:], argspec.defaults))
        except TypeError:
            if argspec.args:
                # No defaults
                positional_count = len(argspec.args)
                defaults = {}
            elif argspec.defaults:
                # Only defaults
                positional_count = 0
                defaults = argspec.defaults

        # Actual decorating
        @wraps(func)
        def _call_wrapper(self, *args, **kwargs):
            used_kwargs = kwargs.copy()

            # Get the used positional arguments given to the function
            used_kwargs.update(zip(argspec.args[positional_count:], args[positional_count:]))

            # Update the dictionary to include the default parameters from the function
            used_kwargs.update({k: used_kwargs.get(k, d) for k, d in defaults.items()})

            # Form the base url, the original function called must return the function name defined in the MBTA api
            function_name = func(self, *args, **kwargs)
            url = f'{PyMBTA3._MBTA_V3_API_URL}/{function_name}'
            for idx, arg_name in enumerate(argspec.args[1:]):
                try:
                    arg_value = args[idx]
                except IndexError:
                    arg_value = used_kwargs[arg_name]

                if arg_value:
                    if arg_name == 'include':
                        if isinstance(arg_value, tuple) or isinstance(arg_value, list):
                            # If the argument is given as list, then we have to format it, you gotta format it nicely
                            arg_value = ','.join(arg_value)
                        url = '{}include={}'.format(url, arg_value)
                    else:
                        # Discard argument in the url formation if it was set to None (in other words, this will call
                        # the api with its internal defined parameter)
                        if isinstance(arg_value, tuple) or isinstance(arg_value, list):
                            # If the argument is given as list, then we have to format it, you gotta format it nicely
                            arg_value = ','.join(arg_value)
                        url = '{}&filter[{}]={}'.format(url, arg_name, arg_value)
            return self._handle_api_call(url)
        return _call_wrapper

    def _handle_api_call(self, url):
        """
        Handle the return call from the  api and return a data and meta_data object. It raises a ValueError on problems
        url:  The url of the service
        """
        response = requests.get(url, headers=self.headers)
        json_response = response.json()
        if not json_response:
            raise ValueError('Error getting data from the api, no return was given.')

        return json_response


class Alerts(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            activity: Union[str, list, tuple] = None,
            route_type: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            stop: Union[str, list, tuple] = None,
            trip: Union[str, list, tuple] = None,
            facility: Union[str, list, tuple] = None,
            id: Union[str, list, tuple] = None,
            banner: bool = None,
            lifecycle: Union[str, list, tuple] = None,
            severity: Union[str, list, tuple] = None,
            datetime: str = None,):
        """
        List active and upcoming system alerts
        https://api-v3.mbta.com/docs/swagger/index.html#/Alert/ApiWeb_AlertController_index
        Keyword Arguments:
        :param include: Relationships to include. [stops, routes, trips, facilities]
        Includes data from related objects in the "included" keyword
        :param activity: An activity affected by an alert. ["BOARD", "USING_ESCALATOR", "PARK_CAR"... ETC]
        :param route_type: Filter by route_type: https://developers.google.com/transit/gtfs/reference/routes-file.
        :param direction_id: Filter by direction of travel along the route.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param stop: Filter by /data/{index}/relationships/stop/data/id
        :param trip: Filter by /data/{index}/relationships/trip/data/id.
        :param facility: Filter by /data/{index}/relationships/facility/data/id.
        :param id: Filter by multiple IDs.
        :param banner: When combined with other filters, filters by alerts with or without a banner.
        :param lifecycle: Filters by an alert’s lifecycle.
        :param severity: Filters alerts by list of severities.
        :param datetime: Filter to alerts that are active at a given time
        Additionally, the string “NOW” can be used to filter to alerts that are currently active.
        """
        _CALL_KEY = "alerts?"
        return _CALL_KEY


class Routes(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            type: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            stop: Union[str, list, tuple] = None,
            trip: Union[str, list, tuple] = None,
            id: Union[str, list, tuple] = None,
            date: str = None):
        """
        List active and upcoming system alerts
        https://api-v3.mbta.com/docs/swagger/index.html#/Route/ApiWeb_RouteController_index
        Keyword Arguments:
        :param include: Relationships to include. [stops, line, route_patterns]
        Includes data from related objects in the "included" keyword
        :param type: Filter by route_type: https://developers.google.com/transit/gtfs/reference/routes-file.
        :param direction_id: Filter by direction of travel along the route.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param stop: Filter by /data/{index}/relationships/stop/data/id
        :param trip: Filter by /data/{index}/relationships/trip/data/id.
        :param id: Filter by multiple IDs.
        :param date: Filter by date that route is active. The active date is the service date. YYYY-MM-DD
        """
        _CALL_KEY = "routes?"
        return _CALL_KEY


class Vehicles(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            route_type: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            label: Union[str, list, tuple] = None,
            trip: Union[str, list, tuple] = None,
            id: Union[str, list, tuple] = None):
        """
        List of vehicles (buses, ferries, and trains)
        https://api-v3.mbta.com/docs/swagger/index.html#/Vehicle/ApiWeb_VehicleController_index
        Keyword Arguments:
        :param include: Relationships to include. [trip, stop, route]
        Includes data from related objects in the "included" keyword
        :param route_type: Filter by route_type: https://developers.google.com/transit/gtfs/reference/routes-file.
        :param direction_id: Filter by direction of travel along the route.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param label: Filter by label.
        :param trip: Filter by /data/{index}/relationships/trip/data/id.
        :param id: Filter by multiple IDs.
        """
        _CALL_KEY = "vehicles?"
        return _CALL_KEY

class Stops(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            date: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            latitude: Union[str, list, tuple] = None,
            longitude: Union[str, list, tuple] = None,
            radius: Union[str, list, tuple] = None,
            id: Union[str, list, tuple] = None,
            route_type: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            service: Union[str, list, tuple] = None,
            location_type: Union[str, list, tuple] = None):
        """
        List of vehicles (buses, ferries, and trains)
        https://api-v3.mbta.com/docs/swagger/index.html#/Vehicle/ApiWeb_VehicleController_index
        Keyword Arguments:
        :param include: Relationships to include. [parent_station, child_stops, recommended_transfers, facilities, route]
        Includes data from related objects in the "included" keyword
        :param date: Filter by date.
        :param direction_id: Filter by direction of travel along the route.
        :param latitude: Latitude in degrees North
        :param longitude: Longitude in degrees East
        :param radius: distance in degrees
        :param id: Filter by multiple IDs.
        :param route_type: Filter by route_type: https://developers.google.com/transit/gtfs/reference/routes-file.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param service: Filter by service id.
        :param location_type: Filter by location type.
        """
        _CALL_KEY = "stops?"
        return _CALL_KEY

class Predictions(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            latitude: Union[str, list, tuple] = None,
            longitude: Union[str, list, tuple] = None,
            radius: Union[str, list, tuple] = None,
            route_pattern: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            stop: Union[str, list, tuple] = None,
            trip: Union[str, list, tuple] = None):
        """
        List of predictions for trips.
        https://api-v3.mbta.com/docs/swagger/index.html#/Prediction/ApiWeb_PredictionController_index
        Keyword Arguments:
        :param include: Relationships to include. [schedule, stop, route, trip, vehicle, alerts]
        Includes data from related objects in the "included" keyword
        :param direction_id: Filter by direction of travel along the route.
        :param latitude: Latitude in degrees North
        :param longitude: Longitude in degrees East
        :param radius: distance in degrees
        :param route_pattern: Filter by /included/{index}/relationships/route_pattern/data/id of a trip.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param stop: Filter by /data/{index}/relationships/stop/data/id.
        :param trip: Filter by /data/{index}/relationships/trip/data/id.
        """
        _CALL_KEY = "predictions?"
        return _CALL_KEY

class Schedules(PyMBTA3):

    @PyMBTA3._call_api_on_func
    def get(self, 
            include: Union[str, list, tuple] = None,
            direction_id: Union[str, list, tuple] = None,
            max_time: Union[str, list, tuple] = None,
            min_time: Union[str, list, tuple] = None,
            route_type: Union[str, list, tuple] = None,
            route: Union[str, list, tuple] = None,
            stop_sequence: Union[str, list, tuple] = None,
            stop: Union[str, list, tuple] = None,
            trip: Union[str, list, tuple] = None):
        """
        List of schedules.
        https://api-v3.mbta.com/docs/swagger/index.html#/Schedule/ApiWeb_ScheduleController_index
        Keyword Arguments:
        :param include: Relationships to include. [stop, route, trip, prediction]
        Includes data from related objects in the "included" keyword
        :param direction_id: Filter by direction of travel along the route.
        :param max_time: Time after which schedule should not be returned.
        :param min_time: Time before which schedule should not be returned.
        :param route_type: Filter by route_type: https://developers.google.com/transit/gtfs/reference/routes-file.
        :param route: Filter by /data/{index}/relationships/route/data/id.
        :param stop: Filter by /data/{index}/relationships/stop/data/id.
        :param stop_sequence: Filter by the index of the stop in the trip.
        :param trip: Filter by /data/{index}/relationships/trip/data/id.
        """
        _CALL_KEY = "schedules?"
        return _CALL_KEY