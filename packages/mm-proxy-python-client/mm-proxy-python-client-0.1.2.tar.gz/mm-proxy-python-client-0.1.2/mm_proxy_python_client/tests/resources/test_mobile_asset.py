import pytest
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_asset import MobileAsset


class MobileAssetTest(unittest.TestCase):
    @pytest.mark.vcr()
    def test_get_asset_by_phone_number_ok(self):
        result = MobileAsset.get_by_phone(phone_number="666888999")
        assert result.phone_number == "666888999"
        assert result.shared_consumption_percentage == 100
        assert result.id == "A8282028202852"
        assert result.pin == "1234"
        assert result.puk == "12345678"
