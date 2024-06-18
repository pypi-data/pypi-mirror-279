from mm_proxy_python_client.client import Client


class MobileAsset:
    _url_path = "get-asset/phone-number/{phone_number}"

    def __init__(self, id, phone, attributes, simAttributes):
        self.id = id
        self.phone_number = phone
        self.pin = simAttributes["PIN"]
        self.puk = simAttributes["PUK"]
        self.shared_consumption_percentage = attributes["Porcentaje_Consumo_Bono_CO"]

    @classmethod
    def get_by_phone(cls, phone_number=""):
        response_data = Client().get(cls._url_path.format(phone_number=phone_number))
        return cls(**response_data)
