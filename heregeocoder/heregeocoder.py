"""
heregeocoder - HERE Geocoder
================================

A Python module that provides two tools to access two basic HERE
Geocoding API functions:
    - get an address from a pair of X/Y coordinates
    - get a pair of X/Y coordinates from an address.
"""

import json

import requests

import here_geocoder_credentials as secret


URL = 'https://geocode.search.hereapi.com/v1/geocode'


class ServiceError(Exception):
    """Raised when there's a problem with Yandex Geocoder."""
    pass


class UnexpectedResponseError(Exception):
    """Raised when a response cannot be parsed using standard scheme."""
    pass


def _form_a_direct_request(address: str) -> dict:
    """Prepare a dictionary of parameters for a direct geocoding
    request.

    Return a dictionary that can be unpacked into the requests.get().
    """
    return {
        'url': URL,
        'params': {
            'q': address,
            'apiKey': secret.APIKEY,
            'lang': 'ru-RU',
            'limit': 1
        }
    }


def _form_a_reverse_request(long_x: float, lat_y: float) -> dict:
    """Prepare a dictionary of parameters for a reverse geocoding
    request.

    Return a dictionary that can be unpacked into the requests.get().
    """
    coord_str = f'{lat_y:.5f}, {long_x:.5f}'
    return {
        'url': URL,
        'params': {
            'at': coord_str,
            'apiKey': secret.APIKEY,
            'lang': 'ru-RU',
            'limit': 1
        }
    }


# STUB
def xy_to_address(long_x: float, lat_y: float) -> tuple:
    """Query HERE for an address given a pair of XY coordinates.

    Returns a tuple of strings representing the geocoding results:
    1. address in Russia as a string,
    2. description of the found object (house, street, area, etc)
    3. geocoding precision level
    """
    request_params = _form_a_reverse_request(long_x, lat_y)
    r = requests.get(**request_params)
    response = r.json()
    if 'error' in response:
        error = response['error']
        message = response['message']
        raise ServiceError(f'{error} / {message}') 
    try:
        result = (
            response['response']['GeoObjectCollection']['featureMember']
            [0]['GeoObject']['metaDataProperty']['GeocoderMetaData']
        )
    except (IndexError, KeyError):
        raise UnexpectedResponseError
    return result['text'], result['kind'], result['precision']


# STUB
def address_to_xy(address: str) -> tuple:
    """Query Yandex for coordinates of an address (in Russia).

    Return a tuple of floats, first being X (Longitude) and second
    being Y (Latitude).
    """
    request_params = _form_a_direct_request(address)
    r = requests.get(**request_params)
    response = r.json()
    if 'error' in response:
        error = response['error']
        message = response['message']
        raise ServiceError(f'{error} / {message}')    
    try:
        coords = (
            response['response']['GeoObjectCollection']['featureMember']
            [0]['GeoObject']['Point']['pos']
        )
    except (IndexError, KeyError):
        raise UnexpectedResponseError
    x_str, y_str = coords.split(' ')
    try:
        x = float(x_str)
        y = float(y_str)
    except ValueError:
        raise UnexpectedResponseError
    return x, y
