import pytest
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_network_status import MobileNetworkStatus


class MobileNetworkStatusTest(unittest.TestCase):
    def _asserts(self, result):
        assert not result.is_roaming_active
        assert result.is_data_active
        assert not result.is_voice_mail_active

    @pytest.mark.vcr()
    def test_get_network_status_by_phone_number_ok(self):
        result = MobileNetworkStatus.get(phone_number="666888999")
        self._asserts(result)

    @pytest.mark.vcr()
    def test_get_network_status_by_asset_id_ok(self):
        result = MobileNetworkStatus.get(asset_id="A8282028202852")
        self._asserts(result)
