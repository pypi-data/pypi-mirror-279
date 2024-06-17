""" atlassible/src/atlassible/myself.py

object with information about me, the user 
"""

import logging

logger = logging.getLogger(__name__)

from atlassible import atl_rest_url
from atlassible.atl_utils import get_resource


def get_me():
    url = atl_rest_url + "myself"
    _, me = get_resource(url)
    return me


## end of file