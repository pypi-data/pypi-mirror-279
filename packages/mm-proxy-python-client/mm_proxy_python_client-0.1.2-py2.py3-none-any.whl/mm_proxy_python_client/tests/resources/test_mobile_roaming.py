import pytest
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_roaming import MobileRoaming


class MobileRoamingTest(unittest.TestCase):
    @pytest.mark.vcr
    def test_activate_roaming_by_phone_number(self):
        assert MobileRoaming.update(phone_number="666888999")

    @pytest.mark.vcr
    def test_activate_roaming_by_asset_id(self):
        assert MobileRoaming.update(asset_id="A8282028202852")

    @pytest.mark.vcr
    def test_not_activatd_roaming(self):
        assert not MobileRoaming.update()
