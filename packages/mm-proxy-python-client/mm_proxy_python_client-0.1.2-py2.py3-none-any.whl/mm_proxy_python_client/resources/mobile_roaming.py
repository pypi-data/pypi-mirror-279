from mm_proxy_python_client.client import Client


class MobileRoaming:
    _url_path = "update-roaming/"

    @classmethod
    def update(cls, asset_id="", phone_number="", activate="True"):
        params = {
            "asset_id": asset_id,
            "phone_number": phone_number,
            "activate": activate,
        }
        response = Client().patch(cls._url_path, **params)

        if response.status_code == 200:
            return True
        return False
