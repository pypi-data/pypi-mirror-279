from mm_proxy_python_client.client import Client


class MobileNetworkStatus:
    _url_path = "get-asset-network-status"

    def __init__(self, is_roaming_active, is_data_active, is_voice_mail_active):
        self.is_roaming_active = is_roaming_active
        self.is_data_active = is_data_active
        self.is_voice_mail_active = is_voice_mail_active

    @classmethod
    def get(cls, asset_id="", phone_number=""):
        params = {
            "asset_id": asset_id,
            "phone_number": phone_number,
        }
        response_data = Client().get(cls._url_path, **params)
        return cls(**response_data)
