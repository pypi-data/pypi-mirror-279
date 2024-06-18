import concurrent.futures

from DataServices.model.sdk_data_input import SDKDataInput
from DataServices.services.sdk_data_services import SDKDataServices
from DataServices.services.helper.data_transform_util import DataTransformUtil
from DataServices.services.helper.request_director import RequestDirector
#import logging

#from DataServices.util.LogFileHandler import LogFileHandler, setup_logger
from Authentication.services.impl.sdk_authenticate_service_impl import User

from DataServices.util.default_properties import DefaultProperties

#logger = setup_logger()
import logging.config
#from DataServices.config.logging_config import LOGGING_CONFIG
# Configure logging
#logging.config.dictConfig(LOGGING_CONFIG)
# Get the logger
logger = logging.getLogger(__name__)

class SDKDataServicesImpl(SDKDataServices):
    def __init__(self):
        #self.logger = logging.getLogger(self.__class__.__name__)
        self._request_director = RequestDirector()
        self._data_transform_util = DataTransformUtil()
        DefaultProperties.set_default_properties()
        self._default_properties = DefaultProperties()

    #NAME OF THE METHOD TO BE FINALIZED
    def invoke_common_module(self, sdk_data_request, proxy=None):
        username = self._default_properties.USERNAME
        password = self._default_properties.PASSWORD
        client_instance = User()
        token_response1 = client_instance.get_token(username, password)
        bearer_token = token_response1.get("access_token")
        print(bearer_token)
        sdk_proxy = proxy
        data_input = SDKDataInput(
            sdk_proxy=sdk_proxy,
            bearer_token=bearer_token,
            data_requests=sdk_data_request
        )
        return self.invoke_data_service(data_input)



    def invoke_data_service(self, sdk_input_request):
        results = {}
        for mnemonic in sdk_input_request.data_requests.mnemonics:
            results[mnemonic] = self.__process_results(
                sdk_input_request.bearer_token, sdk_input_request.sdk_proxy, sdk_input_request.data_requests.function,
                sdk_input_request.data_requests.identifiers, mnemonic, sdk_input_request.data_requests.properties
            )
        # Call convert_to_dataframe with the values dictionary
        #df = self._data_transform_util.convert_to_dataframe(results)
        return results



    def __process_results(self, bearer_token, sdk_proxy, function, identifiers, mnemonics, properties):
        result = []
        api_responses = RequestDirector.execute_in_batch(self._request_director, bearer_token, sdk_proxy, function, identifiers, mnemonics, properties)
        threads = []
        # Define a function to process each API response
        def process_response(api_response):
            result.append(DataTransformUtil.aggregate_response(self._data_transform_util, api_response))

        # Create and start threads for processing API responses
        with concurrent.futures.ThreadPoolExecutor(1) as executor:
            futures = [executor.submit(process_response, api_response) for api_response in api_responses]
            concurrent.futures.wait(futures)
        if isinstance(result, list) and all(isinstance(d, dict) for d in result):

            return {key: value for d in result for key, value in d.items()}
        else:
            return result



