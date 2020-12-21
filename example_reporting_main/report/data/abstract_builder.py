from abc import abstractmethod
import requests
from requests import Response

from example_reporting_main.base_logger import logger


class AbstractBuilder:
    """
        abstract class to retrieve the data via Web Service Get
    """
    def __init__(self, url: str) -> None:
        """
        store in a field named data of type dict
        :param url:url of the Web Service
        """
        self.url = url
        self.data = {}

    def get_data(self, refresh: bool = False) -> dict:
        """
        do the call of the Web Service
        if status != 200 or Exception -> stores the error msg in the data field in a key named 'error_msg'
        otherwise the data field contains the data parsed by the child class with the method 'parse_response'

        :param refresh:
        :return:self.data, dict
                if self.data is void or if refresh is True, do the call of the WebService
                otherwise no call -> just return self.data
        """
        if len(self.data) == 0 or refresh:
            try:
                response = requests.get(self.url, timeout=30)
                if 200 != response.status_code:
                    logger.error("response status for " + self.url + " " + str(response.status_code))
                    self.data = {"error_msg": response.text}

                else:
                    self.data = self.parse_response(response)

            except Exception as exc:
                logger.error(exc, exc_info=True)
                self.data = {"error_msg": str(exc)}

        return self.data

    @abstractmethod
    def parse_response(self, response: Response) -> dict:
        """
        abstract method to parse the response
        :param response: 
        :return: dict of the content of the response
        """
        pass
