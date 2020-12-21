from requests import Response

from example_reporting_main.report.data.abstract_builder import AbstractBuilder

from example_reporting_main.base_logger import logger


class ChartBuilder(AbstractBuilder):
    """
    class to parse the response of the Web Service for charts (i.e image)
    """

    def __init__(self, url: str):
        """
        call super.init, cf doc in super class
        :param url:url of the Web Service
        """
        super().__init__(url)

    def parse_response(self, response: Response) -> dict:
        """
        create a dict of the response, add a key 'content' for the bytes content value
        :param response:
        :return:dict
        """
        data = {"content": response.content}
        logger.debug("ChartBuilder parse_response")
        return data
