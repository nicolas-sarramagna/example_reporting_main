import unittest
from unittest import mock
import json

from example_reporting_main.report.data.abstract_builder import AbstractBuilder


class AbstractBuilderTestCase(unittest.TestCase):
    """Tests for AbstractBuilder """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        builder = AbstractBuilder("url")

        self.assertEqual(builder.url, "url")
        self.assertEqual(builder.data, {})

    def mocked_requests_get(*args, **kwargs):
        """ Mock request """

        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                self.text = json_data  # test purpose

            def json(self):
                return self.json_data

        if args[0] == 'urlOK':
            return MockResponse({"key1": "value1"}, 200)
        elif args[0] == 'urlKO':
            return MockResponse({"error_msg": "value2"}, 500)

        raise ValueError("test exception")

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_call_no_data_refresh_off(self, mock_get):
        """ must fill data """
        builder = AbstractBuilder("urlOK")
        builder.get_data(refresh=False)

        self.assertIsNone(builder.data)  # parse_response is pass
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_call_no_data_refresh_on(self, mock_get):
        """ must fill data """
        builder = AbstractBuilder("urlOK")
        builder.data = {"change"}
        builder.get_data(refresh=True)

        self.assertIsNone(builder.data)  # parse_response is pass
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_call_data_refresh_on(self, mock_get):
        """ must fill data with a refresh call """
        builder = AbstractBuilder("urlOK")
        builder.data = {"change"}
        builder.get_data(refresh=True)

        self.assertIsNone(builder.data)  # parse_response is pass
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_not_call_data_refresh_off(self, mock_get):
        """ no call no change in data """
        builder = AbstractBuilder("urlOK")
        builder.data = {"no change"}
        builder.get_data(refresh=False)

        self.assertEqual({"no change"}, builder.data)
        self.assertEqual(len(mock_get.call_args_list), 0)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_response_status_not_200_error_msg_present(self, mock_get):
        """ must fill data with a error_msg key """
        builder = AbstractBuilder("urlKO")
        builder.data = {"change with error"}
        builder.get_data(refresh=True)

        self.assertTrue("error_msg" in builder.data)
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_exception_msg_present(self, mock_get):
        """ must fill data with a error_msg key """
        builder = AbstractBuilder("urlException")
        builder.data = {"change with error"}
        builder.get_data(refresh=True)

        self.assertEqual('{"error_msg": "test exception"}', json.dumps(builder.data))
        self.assertEqual(len(mock_get.call_args_list), 1)
