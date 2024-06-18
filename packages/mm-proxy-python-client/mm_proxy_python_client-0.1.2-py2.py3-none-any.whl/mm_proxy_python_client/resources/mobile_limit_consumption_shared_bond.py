from mm_proxy_python_client.client import Client


class MobileLimitConsumptionSharedBond:
    _url_path = "update-limit-consumption-shared-bond/"

    @classmethod
    def update(cls, asset_id="", phone_number="", consumption_limit=""):
        params = {
            "asset_id": asset_id,
            "phone_number": phone_number,
            "consumption_limit": consumption_limit,
        }

        response = Client().patch(cls._url_path, **params)

        if response.status_code == 200:
            return True
        return False
