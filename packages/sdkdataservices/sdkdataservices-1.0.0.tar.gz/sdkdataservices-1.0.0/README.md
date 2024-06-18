# DataServices Module

The DataServices Module is a Python library that is common module for Financials and MarketData. It receives SDKDataInput from the two modules and takes care of the rest i.e. sending request to GDSAPI, receiving response in standard GDS response format. Finally, it unpacks the response from GDSAPI to dataframe and returns it as final response.

## Features

- invoke_data_service() is the entry point which will be invoked by Fin/Mkt data
- SDKDataRequest will have the mandatory arguments for GDSAPI i.e. functions, properties, mnamonics and identifiers
- invoke_data_service() will receive SDKDataInput which will contain token, proxy(if received from Fin/Mkt) and SDKDataRequest and forward this SDKDataInput to the rest of the functions, where sending of request to GDSAPI, receiving response, converting the response to dataframe will happen.
- Errors are well handled at every method.

## Installation

You can install the package using pip. Ensure you have Python 3.12+ installed.

```sh
pip install "--path--/Dataservices"
```

## Basic Usage
Here's a brief example of how to use this package:

```sh
from DataServices.model.sdk_data_input import SDKDataInput
from DataServices.model.sdk_data_request import SDKDataRequest
from DataServices.model.sdk_proxy import SDKProxy
from DataServices.services.impl.sdk_data_services_impl import SDKDataServicesImpl


# Create an instance of main class
sdk_data_services_impl = SDKDataServicesImpl()

# Define proxy settings
sdk_proxy = SDKProxy(proxy_username=None, proxy_password=None, proxy_host='proxy_host', proxy_port=8080)

# invoke the entry point method i.e. invoke_data_service by passing SDKDataInput like: 
sdk_data_request = SDKDataRequest(function="GDSP",properties={},identifiers=["aAPL:","IBM"],mnemonics=["IQ_FILINGDATE_IS","IQ_EBITDA"])
sdk_data_input = SDKDataInput(token, proxy, sdk_data_request)
final_output = sdk_data_services_impl.invoke_data_service(sdk_data_input)
print(final_output)


```