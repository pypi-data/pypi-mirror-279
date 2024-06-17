""" atlassible/src/atlassible/atl_util.py 

"""

import logging

logger = logging.getLogger(__name__)

import json 
import requests

from atlassible import atl_creds, atl_rest_url


def get_object_from_json_string(jstr: str) -> object:
    try:
        return json.loads(jstr)
    except Exception as ex:
        logger.exception(f"not a JSON string.  beginning of string is <{jstr[:16]}>")
        return None


def get_resource(url: str, convert_payload: bool = True) -> tuple[requests.Response, dict]:
    """
    only return the resource if the status_code is 2xx.
    this eliminates having to check in the calling methods.

    convert_payload default to True assumes the resource is an actual resource,
    not a response with pagination meta-data and a list of resources.
    For queries expecting pagination, set convert_payload to False.
    
    Return is the Response object and the payload text converted to an object
    if convert_payload was true, else return None for the payload object
    if resp was not ok, return None for both objects
    """
    try:
        logger.debug(f"getting {url}, convertPayload: {convert_payload}")
        resp = requests.get(url, auth=atl_creds)
        if resp is None:
            logger.error(f"None returned for query to {url}")
            return (None, None)
        if not resp.ok:
            logger.warning(
                f"query to {url}, returned status code/reason/text: {resp.status_code}, {resp.reason}, {resp.text}"
            )
            return None, None
        if convert_payload:
            return resp, get_object_from_json_string(resp.text)
        else:
            return resp, None
    except Exception as exec:
        logger.exception(f"Caught exception on query to {url}.")
    return None, None
