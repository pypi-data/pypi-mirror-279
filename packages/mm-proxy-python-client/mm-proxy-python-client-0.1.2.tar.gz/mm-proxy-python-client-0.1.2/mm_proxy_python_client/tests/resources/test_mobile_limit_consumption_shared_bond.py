import pytest
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_limit_consumption_shared_bond import (
    MobileLimitConsumptionSharedBond,
)


class MobileLimitConsumptionSharedBondTest(unittest.TestCase):
    @pytest.mark.vcr
    def test_set_limit_consumption_by_phone_number(self):
        assert MobileLimitConsumptionSharedBond.update(
            phone_number="666888999", consumption_limit="50"
        )

    @pytest.mark.vcr
    def test_set_limit_consumption_by_asset_id(self):
        assert MobileLimitConsumptionSharedBond.update(
            asset_id="A8282028202852", consumption_limit="25"
        )

    @pytest.mark.vcr
    def test_bad_request_limit_consumption(self):
        assert not MobileLimitConsumptionSharedBond.update()
