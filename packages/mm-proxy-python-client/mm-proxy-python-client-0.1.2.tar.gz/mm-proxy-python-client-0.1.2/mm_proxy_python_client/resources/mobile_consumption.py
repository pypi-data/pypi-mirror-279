from mm_proxy_python_client.client import Client
from mm_proxy_python_client.services.date import Date


class Bond:
    def __init__(self, mm_response):
        self.mm_response = mm_response

    @property
    def bond_id(self):
        return self.mm_response.get("idBono")

    @property
    def name(self):
        return self.mm_response.get("nombreProducto")

    @property
    def data_consumed(self):
        return self.mm_response.get("volumen")

    @property
    def data_available(self):
        return self.mm_response.get("volumenTotal")


class Tariff(Bond):
    def __init__(self, mm_response):
        self.mm_response = mm_response
        super().__init__(mm_response)

    @property
    def minutes_consumed(self):
        return self.mm_response.get("vozNacional")

    @property
    def minutes_available(self):
        return self.mm_response.get("vozNacionalTotal")


class MobileConsumption:
    _url_path = "get-asset-consumption"

    def __init__(self, asset_id, consumptions, start_date, end_date):
        self.asset_id = asset_id
        self.start_date = start_date
        self.end_date = end_date
        self.tariffs = [Tariff(item) for item in consumptions["Tariffs"]]
        self.bonds = [Bond(item) for item in consumptions["Bonds"]]

    @classmethod
    def get(cls, asset_id="", phone_number="", start_date=None, end_date=None):
        if not start_date:
            start_date = Date.first_day_this_month()
        if not end_date:
            end_date = Date.today()

        params = {
            "asset_id": asset_id,
            "phone_number": phone_number,
            "start_date": start_date,
            "end_date": end_date,
        }
        response_data = Client().get(cls._url_path, **params)

        return cls(**response_data, start_date=start_date, end_date=end_date)
