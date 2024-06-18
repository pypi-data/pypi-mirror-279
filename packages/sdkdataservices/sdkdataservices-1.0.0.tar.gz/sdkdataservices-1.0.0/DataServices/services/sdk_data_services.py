from abc import ABC, abstractmethod

class SDKDataServices(ABC):
    @abstractmethod
    def invoke_data_service(self, sdk_input_request):
        pass

