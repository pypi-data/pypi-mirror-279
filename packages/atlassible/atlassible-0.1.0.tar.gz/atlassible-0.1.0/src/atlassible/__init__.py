""" atlassible/src/atlassible/__init__.py 
"""

# read version from installed package
from importlib.metadata import version

__version__ = version("atlassible")

import os


atl_user = os.getenv("ATLASSIAN_USER", "ATLASSIAN_USER is missing")
atl_token = os.getenv("ATLASSIAN_API_TOKEN", "ATLASSIAN_API_TOKEN is missing")
atl_base_url = os.getenv("ATLASSIAN_BASE_URL", "ATLASSIAN_BASE_URL is missing")
atl_api_url = os.getenv("ATLASSIAN_API_URL", "/rest/api/3/")
atl_rest_url = atl_base_url + atl_api_url
atl_creds = (atl_user, atl_token)

from atlassible import myself 

## end of file 