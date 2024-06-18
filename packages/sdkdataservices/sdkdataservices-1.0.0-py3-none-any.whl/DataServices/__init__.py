from DataServices.model.sdk_data_input import SDKDataInput
from DataServices.model.sdk_data_request import SDKDataRequest
from DataServices.model.sdk_proxy import SDKProxy
from DataServices.services.impl.sdk_data_services_impl import SDKDataServicesImpl
import pandas as pd
#from authentication_module.services.impl.sdk_authenticate_service_impl import User
'''
username = "--username--"
password = "--password--"
client_instance = User()

#get_token()
token_response1 = client_instance.get_token(username, password)
bearer_token = token_response1.get("access_token")'''
#ref_token = token_response1.get("refresh_token")
#token_response2 = client_instance.get_refresh_token(ref_token)
#Sample requests we would recieve from Fin and Mkt data modules
sdk_proxy = SDKProxy()

request1 = SDKDataRequest(
    function="GDSP",
    properties={},
    identifiers=["aAPL:","IBM", "Walmart","BV7KKK9","BGSCL06","6112482","6101101","BYVC6Y8","6143255","BF1BKG2"],
    mnemonics=["IQ_FILINGDATE_IS","IQ_EBITDA","IQ_NI","IQ_TOTAL_REV","IQ_EBIT","IQ_COGS","IQ_GROSS_MARGIN","IQ_DILUT_EPS_EXCL","IQ_GP",
"IQ_PERIODDATE"]
)

request2 = SDKDataRequest(
    function="GDST",
    identifiers=["IBM"],
    mnemonics=["IQ_EBIT"]
)
request3 = SDKDataRequest(
    function="GDSHE",
    properties={"periodType":"IQ_FQ-4"},
    identifiers=["aAPL:","IBM", "Walmart"],
    mnemonics=["IQ_FILINGDATE_IS","IQ_EBITDA","IQ_NI","IQ_TOTAL_REV","IQ_EBIT","IQ_COGS","IQ_GROSS_MARGIN","IQ_DILUT_EPS_EXCL","IQ_GP",
"IQ_PERIODDATE"]
)


'''
data_input = SDKDataInput(
    sdk_proxy=sdk_proxy,
    bearer_token=bearer_token,
    data_requests=request2
)'''


sdk_data_services_impl = SDKDataServicesImpl()
data = sdk_data_services_impl.invoke_common_module(request1,sdk_proxy)
print(data)

