import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("Authorization", "DUMMY")],
    }


@pytest.fixture(autouse=True)
def define_env(monkeypatch):
    monkeypatch.setenv("MM_PROXY_BASEURL", "http://somconnexio-mm-proxy.local:8000")
    monkeypatch.setenv("MM_PROXY_USER", "mm-proxy")
    monkeypatch.setenv("MM_PROXY_PASSWORD", "FAKE-PASSWORD")
