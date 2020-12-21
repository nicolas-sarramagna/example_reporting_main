import json

from requests import Response

from example_reporting_main.report.data.abstract_builder import AbstractBuilder

from example_reporting_main.base_logger import logger


class IndicatorBuilder(AbstractBuilder):
    """
    class to parse the response of the Web Service for indicators (i.e values)
    """

    def __init__(self, url: str):
        """
        call super.init, cf doc in super class
        :param url:url of the Web Service
        """
        super().__init__(url)

    def parse_response(self, response: Response) -> dict:
        """
        parse json response to dict
        :param response:
        :return:dict
        """
        data = json.loads(response.json())
        # same order between calls
        data['details'].sort(key=lambda x: x['trend_name'])
        logger.debug("IndicatorBuilder parse_response")
        logger.debug(data)

        return data
