import pytest
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_data_service import MobileDataService


class MobileServiceDataTest(unittest.TestCase):
    @pytest.mark.vcr
    def test_activate_data_service_by_phone_number(self):
        assert MobileDataService.update(phone_number="666888999")

    @pytest.mark.vcr
    def test_activate_data_service_by_asset_id(self):
        assert MobileDataService.update(asset_id="A8282028202852")

    @pytest.mark.vcr
    def test_not_activated_data_service(self):
        assert not MobileDataService.update()
