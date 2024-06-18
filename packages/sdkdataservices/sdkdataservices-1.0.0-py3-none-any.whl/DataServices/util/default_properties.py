import logging
from DataServices.util.property_utils import PropertyUtils
from DataServices.constants.sdk_constants import SDKConstants
logger = logging.getLogger(__name__)

class DefaultProperties:
    REST_BY_JSON_URL = None
    BATCH_SIZE = -1
    SDK_CLIENT_VERSION = None
    MAX_THREADS = -1
    USERNAME = None
    PASSWORD = None


    @staticmethod
    def set_default_properties():
        try:
            DefaultProperties.REST_BY_JSON_URL = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.SDK_REST_JSON_URL)
            logger.info(f"SDK JSON URL is configured with : {DefaultProperties.REST_BY_JSON_URL}")

            DefaultProperties.SDK_CLIENT_VERSION = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.PROP_CLIENT_VERSION)
            logger.info(f"SDK Client Library VERSION is configured with : {DefaultProperties.SDK_CLIENT_VERSION}")

            DefaultProperties.BATCH_SIZE = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.BATCH_SIZE)
            logger.info(f"SDK Client Batch Size is configured with : {DefaultProperties.BATCH_SIZE}")

            DefaultProperties.MAX_THREADS = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.MAX_THREADS)
            #logger.info(f"SDK Client max threads is configured with : {DefaultProperties.MAX_THREADS}")

            DefaultProperties.USERNAME = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.USERNAME)
            #logger.info(f"SDK Client username for auth module is configured with : {DefaultProperties.USERNAME}")

            DefaultProperties.PASSWORD = PropertyUtils.get_property(SDKConstants.SDK, SDKConstants.PASSWORD)
            #logger.info(f"SDK Client password for auth module is configured with : {DefaultProperties.PASSWORD}")

        except Exception as e:
            logger.error("Error while reading default properties from spciq-api-dataservices-application.properties. Please set the properties properly.", exc_info=True)
