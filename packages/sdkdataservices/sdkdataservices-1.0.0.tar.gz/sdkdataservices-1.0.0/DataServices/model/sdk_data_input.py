from typing import List

from DataServices.model.sdk_data_input_base import SDKDataInputBase
from DataServices.model.sdk_data_request import SDKDataRequest
from DataServices.model.sdk_proxy import SDKProxy


class SDKDataInput(SDKDataInputBase):
    def __init__(self, bearer_token: str = None, sdk_proxy: SDKProxy = None,  data_requests: SDKDataRequest = None):
        super().__init__(bearer_token, sdk_proxy)
        #self.bearer_token = bearer_token
        self._data_requests = data_requests

    @property
    def data_requests(self):
        return self._data_requests

    @data_requests.setter
    def data_requests(self, data_requests):
        self._data_requests = data_requests

    def __str__(self):
        return f"Bearer Token: {self.bearer_token},  Data Requests: {self.data_requests}"
