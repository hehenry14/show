import logging
from requests import Request

logger = logging.getLogger(__name__)


class ProductInfo:

    def __init__(self, config: dict, product_id: int):
        """
        This is a object that groups all the relevant info and functionality for the product to be purchaseed.
        :param config: the config of the product.
        :param product_id: the id of the product.
        """
        self._id = product_id
        self._is_valid = True
        self._logger = logger

        try:
            self._product_site = config['product_site']
            self._log_in_xpath = config['log_in_xpath']
            self._purchase_xpath = config['purchase_xpath']
            self._check_out_xpath = config['checkout_xpath']
            self._payment_xpath = config['checkout_xpath']
        except KeyError as e:
            self._logger.error(f"a key is missing this is incorrect {e}")
            self._is_valid = False

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def product_site(self):
        return self._product_site

    def get_login_request(self, credentials: dict) -> Request:
        """
        This function gets the login request structure.
        :return: a http request for log in.
        """
        ...
