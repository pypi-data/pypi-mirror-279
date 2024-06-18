import json
import socket
import requests
import concurrent.futures
from Authentication.services.impl.sdk_authenticate_service_impl import User
from requests.auth import HTTPBasicAuth
import logging
from requests.exceptions import HTTPError, RequestException

from DataServices.services.support.rest_gateway_support import RestGatewaySupport
from DataServices.util.default_properties import DefaultProperties
from DataServices.util.property_utils import PropertyUtils

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class RequestDirector:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        #DefaultProperties.set_default_properties()
        self._default_properties = DefaultProperties()
        self._client_instance = User()

    def execute_in_batch(self, bearer_token, sdk_proxy, function=None, identifiers=None, mnemonics=None, properties={}):
        # Function to create API requests
        if identifiers != None:
            results = []
            requests_to_send = []

            for identifier in identifiers:
                requests_to_send.append({
                    "function": function,
                    "identifier": str(identifier),
                    "mnemonic": mnemonics,
                    "properties": properties,
                })

            request_batches = [
                requests_to_send[i: i + int(self._default_properties.BATCH_SIZE)]
                for i in range(0, len(requests_to_send), int(self._default_properties.BATCH_SIZE))
            ]

            with concurrent.futures.ThreadPoolExecutor(int(self._default_properties.MAX_THREADS)) as executor:
                futures = [executor.submit(self.__send_sdk_request, bearer_token, sdk_proxy, True, batch, results) for batch in request_batches]
                concurrent.futures.wait(futures)

            return results
        else:
            return self.__send_sdk_request(bearer_token, sdk_proxy)

    def __send_sdk_request(self, bearer_token, sdk_proxy, retry=False, batch=None, results=None):
        supported_versions = ["v3"]
        if PropertyUtils.check_version(self._default_properties.REST_BY_JSON_URL, supported_versions):
            payload = {"inputRequests": batch} if batch is not None else ""

            headers = {
                "Content-Type": "application/json",
                "client_version": str(self._default_properties.SDK_CLIENT_VERSION),
                "client_ip": str(self.__get_client_ip()),
                "Authorization": f"Bearer {bearer_token}"
            }

            # Create a session with proxy settings
            session = RestGatewaySupport.create_rest_template(sdk_proxy)
            response_data = None
            response = None

            try:
                # Send the POST request
                response = session.post(
                    self._default_properties.REST_BY_JSON_URL,
                    headers=headers,
                    data=json.dumps(payload)
                )

                # Raise an HTTPError if the response status code indicates an error
                response.raise_for_status()

                # If no exception is raised, process the JSON response
                response_data = response.json()

            except requests.exceptions.HTTPError as http_err:
                if retry:
                    try:
                        # Update the bearer token
                        username = self._default_properties.USERNAME
                        password = self._default_properties.PASSWORD
                        bearer_token = self._client_instance.get_token(username, password).get("access_token")
                        # To be modified while integrating with auth module we will invoke the Auth's funciton

                        # Retry the request with the new token
                        return self.__send_sdk_request(bearer_token, sdk_proxy, retry=False, batch=batch, results=results)
                    except Exception as ex:
                        print("Error while getting the token {}", ex)
                else:
                    if response.status_code == 503:
                        response_data = {"ErrMsg": "Service down"}
                    elif response.status_code == 401:
                        response_data = {"ErrMsg": "Unauthorized"}
                    else:
                        response_data = {"ErrMsg": f"HTTP error occurred: {http_err}"}
            except Exception as err:
                response_data = {"ErrMsg": f"An error occurred: {err}"}

            if results is not None:
                results.append(response_data)
            else:
                return response_data
        else:
            if results is not None:
                results.append({"ErrMsg": "Only v3 version is supported"})
            else:
                return {"ErrMsg": "Only v3 version is supported"}

    def __get_client_ip(self):
        ip_address = ""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except Exception as e:
            logging.error("Exception occurred while getting the IP address", exc_info=True)
        return ip_address


