import logging
import requests
import json

from mm_proxy_python_client import helpers
from mm_proxy_python_client import exceptions


logger = logging.getLogger(__name__)


class Client(object):
    """Client class
    This class manage the HTTP requests and only this class can send a request.

    We need to be able the environment variables needed to connect
    with the MM-proxy instance:
    * MM_PROXY_BASEURL
    * MM_PROXY_USER
    * MM_PROXY_PASSWORD
    """

    def __init__(self):
        self.baseurl = helpers.getenv_or_fail("MM_PROXY_BASEURL")
        self.user = helpers.getenv_or_fail("MM_PROXY_USER")
        self.password = helpers.getenv_or_fail("MM_PROXY_PASSWORD")

    def get(self, route, **kwargs):
        """Send a GET HTTP requests

        Args:
            route (str): String with the path to the route
            kwargs (dict): key-word values to send as paramethers

        Return:
            **response**: Return the response content as json
        """
        return self._send_request(
            verb="GET",
            url=self._format_url(route),
            params=kwargs,
        ).json()

    def patch(self, route, **kwargs):
        """Send a PATCH HTTP requests

        Args:
            route (str): String with the path to the route
            kwargs (dict): key-word values to send in the body of the request

        Return:
            **response**: Return the response object
        """
        return self._send_request(
            verb="PATCH",
            url=self._format_url(route),
            payload=kwargs,
            extra_headers={
                "Content-Type": "application/json",
            },
        )

    def _send_request(self, verb, url, payload=None, params={}, extra_headers={}):
        """send the API request using the *requests.request* method

        Args:
            payload (dict)

        Raises:
            HTTPError

        Returns:
            **requests.Response**: Response received after sending the request.

        .. note::
            Supported HTTP Methods: DELETE, GET, HEAD, PATCH, POST, PUT
        """

        headers = {
            "Accept": "application/json",
        }

        json_payload = None
        if payload:
            json_payload = json.dumps(payload)

        if extra_headers:
            headers.update(extra_headers)

        try:
            response = requests.request(
                verb.upper(),
                url,
                headers=headers,
                data=json_payload,
                params=params,
                auth=(self.user, self.password),
            )
        except Exception as err:
            raise exceptions.HTTPError(err)

        return response

    def _format_url(self, route):
        return "{url}/{path_prefix}/{route}".format(
            url=self.baseurl, path_prefix="api", route=route
        )
