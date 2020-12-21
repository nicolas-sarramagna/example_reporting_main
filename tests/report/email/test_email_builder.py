import unittest
import unittest.mock
from unittest.mock import patch

from example_reporting_main.report.email.email_builder import EmailBuilder
from email.mime.multipart import MIMEMultipart


class EmailBuilderTestCase(unittest.TestCase):
    """Tests for EmailBuilder"""

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email",
                                     True, "secure_mode_login", "secure_mode_pwd")

        self.assertEqual(email_builder.smtp_host, "localhost")
        self.assertEqual(email_builder.smtp_port, 8000)
        self.assertEqual(email_builder.sender_email, "sender_email")
        self.assertEqual(email_builder.receiver_email, "receiver_email")
        self.assertEqual(email_builder.is_secure_mode, True)
        self.assertEqual(email_builder.secure_mode_login, "secure_mode_login")
        self.assertEqual(email_builder.secure_mode_pwd, "secure_mode_pwd")

    def test_constructor_check_optional_fields(self):
        """ must put defautl values in fields not present in parameter """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")

        self.assertEqual(email_builder.smtp_host, "localhost")
        self.assertEqual(email_builder.smtp_port, 8000)
        self.assertEqual(email_builder.sender_email, "sender_email")
        self.assertEqual(email_builder.receiver_email, "receiver_email")
        self.assertEqual(email_builder.is_secure_mode, False)
        self.assertEqual(email_builder.secure_mode_login, "")
        self.assertEqual(email_builder.secure_mode_pwd, "")

    def test_add_image_void_no_action(self):
        """ message payload must be void """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        message = MIMEMultipart()

        email_builder._add_image(None, message)
        self.assertTrue(0 == len(message.get_payload()))

        email_builder._add_image([], message)
        self.assertTrue(0 == len(message.get_payload()))

    def test_add_image_file_not_empty(self):
        """ message payload must be not emppty  """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        message = MIMEMultipart()
        email_builder._add_image([b'01'], message)

        self.assertTrue(1 == len(message.get_payload()))

    def test_add_one_image_file_check_fields(self):
        """ message payload must have a image header  """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        message = MIMEMultipart()
        email_builder._add_image([b'01'], message)
        base = message.get_payload()[0]
        base_str = base.as_string()

        self.assertTrue('image/png' in base_str)
        self.assertTrue('filename="chart-image0.png"' in base_str)
        self.assertTrue('X-Attachment-Id: 0' in base_str)
        self.assertTrue('Content-ID: <0>' in base_str)

    def test_add_two_images_file_check_fields(self):
        """ message payload must have two images header  """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        message = MIMEMultipart()
        email_builder._add_image([b'0', b'0'], message)

        self.assertTrue(2 == len(message.get_payload()))

        for idx, base in enumerate(message.get_payload()):
            base_str = base.as_string()
            idx_str = str(idx)

            self.assertTrue('image/png' in base_str)
            self.assertTrue('filename="chart-image' + idx_str + '.png"' in base_str)
            self.assertTrue('X-Attachment-Id: ' + idx_str in base_str)
            self.assertTrue('Content-ID: <' + idx_str + '>' in base_str)

    def test_server_email_secure_called(self):
        """ test smtplib.SMTP_SSL call  """
        # Mock 'smtplib.SMTP_SSL' class
        with unittest.mock.patch('smtplib.SMTP_SSL', autospec=True) as mock_smtp:
            email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email", True)
            message = MIMEMultipart()
            email_builder._server_email(message)
            instance = mock_smtp.return_value.__enter__.return_value
            name, args, kwargs = instance.method_calls.pop(0)

            self.assertEqual(name, 'login')
            name, args, kwargs = instance.method_calls.pop(0)
            self.assertEqual(name, 'sendmail')
            # Validate the sendmail() parameters
            from_, to_, body_ = args
            self.assertEqual('sender_email', from_)
            self.assertEqual('receiver_email', to_)

    def test_server_email_unsecure_called(self):
        """ test smtplib.SMTP call  """
        # Mock 'smtplib.SMTP' class
        with unittest.mock.patch('smtplib.SMTP', autospec=True) as mock_smtp:
            email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email", False)
            message = MIMEMultipart()
            email_builder._server_email(message)
            instance = mock_smtp.return_value.__enter__.return_value
            name, args, kwargs = instance.method_calls.pop(0)

            self.assertEqual(name, 'sendmail')
            # Validate the sendmail() parameters
            from_, to_, body_ = args
            self.assertEqual('sender_email', from_)
            self.assertEqual('receiver_email', to_)

    def test_create_mime_object(self):
        """must create the mime object for email"""
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        mime_object = email_builder._create_message_email("html message")
        mime_object_str = mime_object.as_string()

        self.assertTrue(mime_object.is_multipart())
        self.assertEqual("multipart/alternative", mime_object.get_content_type())
        self.assertTrue("From: sender_email" in mime_object_str)
        self.assertTrue("To: receiver_email" in mime_object_str)
        self.assertTrue("Subject: Daily Report Bitcoin - USD" in mime_object_str)
        self.assertTrue("Content-Type: text/html;" in mime_object_str)

    @patch('example_reporting_main.report.email.email_builder.EmailBuilder._create_message_email', autospec=True)
    @patch('example_reporting_main.report.email.email_builder.EmailBuilder._add_image', autospec=True)
    @patch('example_reporting_main.report.email.email_builder.EmailBuilder._server_email', autospec=True)
    def test_send_email_general(self, mock1, mock2, mock3):
        """must call internal methods """
        email_builder = EmailBuilder("localhost", 8000, "sender_email", "receiver_email")
        email_builder.send_email(msg_html="msg html")

        self.assertEqual(1, mock1.call_count)
        self.assertEqual(1, mock2.call_count)
        self.assertEqual(1, mock3.call_count)
