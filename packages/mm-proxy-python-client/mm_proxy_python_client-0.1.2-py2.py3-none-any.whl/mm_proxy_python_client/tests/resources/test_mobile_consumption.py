from __future__ import unicode_literals  # support both Python2 and 3

import pytest
from mock import patch, Mock
import unittest2 as unittest

from mm_proxy_python_client.resources.mobile_consumption import (
    MobileConsumption,
    Tariff,
    Bond,
)

MOCKED_DATE = {"first_day_this_month": "2024-01-01", "today": "2024-01-15"}


@patch.multiple(
    "mm_proxy_python_client.resources.mobile_consumption.Date",
    first_day_this_month=Mock(return_value=MOCKED_DATE["first_day_this_month"]),
    today=Mock(return_value=MOCKED_DATE["today"]),
)
class MobileConsumptionTests(unittest.TestCase):
    @pytest.mark.vcr
    def test_get_consumption_by_phone_number(self):
        result = MobileConsumption.get(phone_number="666888999")

        assert result.start_date == MOCKED_DATE["first_day_this_month"]
        assert result.end_date == MOCKED_DATE["today"]

        # Tariffs
        assert type(result.tariffs) == list
        assert len(result.tariffs) == 1

        tariff = result.tariffs[0]
        assert type(tariff) == Tariff
        assert tariff.name == "Tarifa MAGNIFICA 5"
        assert tariff.bond_id == "B0393"
        assert tariff.data_consumed == "342"
        assert tariff.data_available == "5120"
        assert tariff.minutes_consumed == "114"
        assert tariff.minutes_available == "ILIM"

        # Bond
        assert type(result.bonds) == list
        assert len(result.bonds) == 1

        bond = result.bonds[0]
        assert type(bond) == Bond
        assert bond.name == "Bono 1 GB Adicional"
        assert bond.bond_id == "B0715"
        assert bond.data_consumed == "0"
        assert bond.data_available == "1024"

    @pytest.mark.vcr
    def test_get_consumption_by_asset_id(self):
        result = MobileConsumption.get(asset_id="02i4I00000b9JTOQA2")

        assert result.start_date == MOCKED_DATE["first_day_this_month"]
        assert result.end_date == MOCKED_DATE["today"]

        # Tariffs
        assert type(result.tariffs) == list
        assert len(result.tariffs) == 1

        tariff = result.tariffs[0]
        assert type(tariff) == Tariff
        assert tariff.name == "Tarifa MAGNIFICA 5"
        assert tariff.bond_id == "B0393"
        assert tariff.data_consumed == "342"
        assert tariff.data_available == "5120"
        assert tariff.minutes_consumed == "114"
        assert tariff.minutes_available == "ILIM"

        # Bond
        assert type(result.bonds) == list
        assert len(result.bonds) == 1

        bond = result.bonds[0]
        assert type(bond) == Bond
        assert bond.name == "Bono 1 GB Adicional"
        assert bond.bond_id == "B0715"
        assert bond.data_consumed == "0"
        assert bond.data_available == "1024"

    @pytest.mark.vcr()
    def test_get_consumption_with_dates(self):
        custom_start_date = "2023-12-01"
        custom_end_date = "2023-12-31"

        result = MobileConsumption.get(
            asset_id="02i4I00000b9JTOQA2",
            start_date=custom_start_date,
            end_date=custom_end_date,
        )

        assert result.start_date == custom_start_date
        assert result.end_date == custom_end_date
