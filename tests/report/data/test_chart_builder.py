import unittest

import requests

from example_reporting_main.report.data.chart_builder import ChartBuilder


class ChartBuilderTestCase(unittest.TestCase):
    """Tests for ChartBuilder """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        builder = ChartBuilder("url")

        self.assertEqual(builder.url, "url")
        self.assertEqual(builder.data, {})

    def test_parse_response_build_data(self):
        """ build data with content key  """
        builder = ChartBuilder("url")
        response = requests.Response()
        result_call = builder.parse_response(response)

        self.assertTrue('content' in result_call)
