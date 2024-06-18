from mock import patch
import unittest2 as unittest

import json
import os
import requests

from mm_proxy_python_client.client import Client
from mm_proxy_python_client import exceptions


REQUIRED_ENVVARS = {
    "MM_PROXY_BASEURL": "http://my-mm-proxy",
    "MM_PROXY_USER": "mm-user",
    "MM_PROXY_PASSWORD": "mm-password",
}


class FakeRequest:
    method = ""
    url = ""

    def __init__(self, method="GET", url="some-url"):
        self.method = method
        self.url = url


class FakeResponse:
    status_code = None
    content = ""
    reason = ""
    request = FakeRequest()

    def __init__(self, status=200, reason="", content="{}"):
        self.status_code = status
        self.content = content
        self.reason = reason

    def json(self):
        return json.loads(self.content)


@patch.dict("os.environ", REQUIRED_ENVVARS)
class ClientTests(unittest.TestCase):
    sample_route = "path"
    baseurl = REQUIRED_ENVVARS.get("MM_PROXY_BASEURL")
    user = REQUIRED_ENVVARS.get("MM_PROXY_USER")
    pswd = REQUIRED_ENVVARS.get("MM_PROXY_PASSWORD")

    def test_init_has_not_envvars_defined_raises_exception(self):
        with self.assertRaises(Exception):
            for envvar in REQUIRED_ENVVARS.keys():
                os.environ.pop(envvar)
                Client()

    @patch.object(requests, "request", side_effect=Exception())
    def test_network_error_raises_expected_exception(self, _):
        self.assertRaises(exceptions.HTTPError, Client().get, self.sample_route)

    @patch.object(requests, "request", return_value=FakeResponse())
    def test_get(self, mock_request):
        Client().get(self.sample_route, param1="1", param2="2")

        mock_request.assert_called_once_with(
            "GET",
            self.baseurl + "/api/" + self.sample_route,
            headers={
                "Accept": "application/json",
            },
            data=None,
            params={"param1": "1", "param2": "2"},
            auth=(self.user, self.pswd),
        )

    @patch.object(requests, "request", return_value=FakeResponse())
    def test_patch(self, mock_request):
        Client().patch(self.sample_route, param1="1", param2="2")

        mock_request.assert_called_once_with(
            "PATCH",
            self.baseurl + "/api/" + self.sample_route,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data='{"param1": "1", "param2": "2"}',
            params={},
            auth=(self.user, self.pswd),
        )

    @patch.object(requests, "request", return_value=FakeResponse())
    def test_url_format(self, mock_request):
        new_url = "http://new-url"
        os.environ["MM_PROXY_BASEURL"] = new_url
        Client().get(self.sample_route)

        mock_request.assert_called_once_with(
            "GET",
            new_url + "/api/" + self.sample_route,
            headers={
                "Accept": "application/json",
            },
            data=None,
            params={},
            auth=(self.user, self.pswd),
        )
