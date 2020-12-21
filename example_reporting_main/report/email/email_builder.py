import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from typing import List

from example_reporting_main.base_logger import logger


class EmailBuilder:
    """
        class to send email
    """

    def __init__(self, smtp_host: str, smtp_port: int, sender_email: str, receiver_email: str,
                 is_secure_mode: bool = False, secure_mode_login: str = "", secure_mode_pwd: str = "") -> None:
        """
            set sender and receiver in instance
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.is_secure_mode = is_secure_mode
        self.secure_mode_login = secure_mode_login
        self.secure_mode_pwd = secure_mode_pwd

    def send_email(self, msg_html: str, data_img: List[bytes] = None) -> None:
        """
        Send email in multipart mode (plain + html) with images

        :param msg_html: html msg string to send
        :param data_img: images content to add in the mail
        :return:None
        """

        logger.debug("create mime email object")
        message = self._create_message_email(msg_html)

        logger.debug("add image in email")
        self._add_image(data_img, message)

        logger.debug("proceed to send email")
        self._server_email(message)

    def _create_message_email(self, msg_html: str) -> MIMEMultipart:
        """
        create the MimeMultipart message to send
        :param msg_html: html msg string to send
        :return: the MimeMultipart message
        """
        message = MIMEMultipart("alternative")

        message["Subject"] = "Daily Report Bitcoin - USD"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        message.attach(MIMEText(msg_html, "html", "utf-8"))
        return message

    def _server_email(self, message: MIMEMultipart) -> None:
        """
            use server smtp to send the email
            if is_secure_mode is True, use a ssl context to send the email
        :param message: the message to send
        :return: None
        """
        if self.is_secure_mode:
            # Create secure SSL context
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context) as server:
                logger.debug("Connect to secure smtp server")
                server.login(self.secure_mode_login, self.secure_mode_pwd)
                logger.debug("send secure email from " + self.sender_email + " to " + self.receiver_email)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
        else:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                logger.debug("send email from " + self.sender_email + " to " + self.receiver_email)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())

    def _add_image(self, data_img: List[bytes], message: MIMEMultipart) -> None:
        """
        add images in email
        :param data_img: images content to add in the mail
        :param message: email to add images
        :return:None
        """
        if data_img is None:
            data_img = []
        for idx, img_bytes in enumerate(data_img):
            # set attachment mime
            filename = 'chart-image' + str(idx) + '.png'
            logger.debug("create mime for image " + filename)
            mime = MIMEBase('image', 'png', filename=filename)
            # add required header
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('X-Attachment-Id', str(idx))
            mime.add_header('Content-ID', '<' + str(idx) + '>')
            # put content  into MIMEBase object
            mime.set_payload(img_bytes)
            encoders.encode_base64(mime)
            # add MIMEBase to MIMEMultipart object
            message.attach(mime)

        logger.debug("add image in email DONE with " + str(len(data_img)) + " images")
