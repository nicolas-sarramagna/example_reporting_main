import json
import unittest

import requests

from example_reporting_main.report.data.indicator_builder import IndicatorBuilder


class IndicatorBuilderTestCase(unittest.TestCase):
    """Tests for IndicatorBuilder """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        builder = IndicatorBuilder("url")

        self.assertEqual(builder.url, "url")
        self.assertEqual(builder.data, {})

    def test_parse_response_result_same_order(self):
        """ multiple parsing return same order in json  """
        builder = IndicatorBuilder("url")

        response = requests.Response()
        data_json = '{"details": [{"trend_name": "aa"}, {"trend_name": "ab"}, {"trend_name": "ac"}]}'

        def json_func() -> str:
            return data_json

        response.json = json_func

        result_call = builder.parse_response(response)
        self.assertEqual(data_json, json.dumps(result_call))

        data_json_correct_order = str(data_json)
        # json not result order
        data_json = '{"details": [{"trend_name": "ab"}, {"trend_name": "ac"}, {"trend_name": "aa"}]}'
        result_call = builder.parse_response(response)
        self.assertEqual(data_json_correct_order, json.dumps(result_call))
