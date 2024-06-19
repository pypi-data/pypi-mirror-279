import requests
import json
import urllib
import os
import io

def attribute_allowed_list(value: str, allowed_list: list, raise_exception=False, hint='') -> bool:
    """Checks if a value is in a list of accepted values. Will raise a ValueError exception when raise_exception is true."""
    if value in allowed_list:
        return True
    if raise_exception:
        raise ValueError(f'{hint}Expected {allowed_list} but got {value}')
    return False

def validate_attribute_allowed_list(value: str, allowed_list: list, raise_exception=True, hint='') -> str:
    """Checks if a value is in a list of accepted values. Will raise a ValueError exception when raise_exception is true. Otherwise return None"""
    if value in allowed_list:
        return value
    if raise_exception:
        raise ValueError(f'{hint}Expected {allowed_list} but got {value}')
    return None

class APIException(Exception):
    """This is a catchall for API Errors. json response should be available via the extra_data attribute."""
    def __init__(self, Exception, extra_data=None):
        self.extra_data = extra_data


class TeamsHelper:
    def __init__(self, authorization_token: str, base_url: str='https://graph.microsoft.com/v1.0', log_level='INFO'):
        """Allows interaction with a teams site"""
        pass