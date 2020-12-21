import unittest
from os import path

from example_reporting_main.report.email.message_builder import MessageBuilder


class MessageBuilderTestCase(unittest.TestCase):
    """Tests for MessageBuilder"""

    TEMPLATE_FILE = "template_mail_test/template_test.html"

    def test_read_template_is_not_none(self):
        """Must template not null"""
        template_path = path.join(path.dirname(path.abspath(__file__)), MessageBuilderTestCase.TEMPLATE_FILE)
        msg_builder = MessageBuilder(template_path)

        self.assertIsNotNone(msg_builder.template)

    def test_render_template_replace_var_return_str(self):
        """ Must replace var and return str """
        template_path = path.join(path.dirname(path.abspath(__file__)), MessageBuilderTestCase.TEMPLATE_FILE)
        msg_builder = MessageBuilder(template_path)
        msg = msg_builder.build_message({"var_summary": "my_summary_value"})

        self.assertEqual("<h1>indicators my_summary_value</h1>", msg)
