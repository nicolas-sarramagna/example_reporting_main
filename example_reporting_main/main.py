import os
import configparser
from os import path

from example_reporting_main.report.data.chart_builder import ChartBuilder
from example_reporting_main.report.data.indicator_builder import IndicatorBuilder
from example_reporting_main.report.email.email_builder import EmailBuilder
from example_reporting_main.report.email.message_builder import MessageBuilder

from distutils.util import strtobool
from example_reporting_main.base_logger import logger

if __name__ == '__main__':
    # 0 . Load config file
    config = configparser.ConfigParser()

    # for circleci which do not support volumes
    config_folder = os.getenv("config_folder", "config")

    config_file_path = path.join(path.dirname(path.abspath(__file__)), config_folder + "/config.cfg")
    config.read(config_file_path)
    logger.info("Read config file DONE")

    # 1 . Get data
    host = config.get("AppSection", "web_service_host")
    port = int(config.get("AppSection", "web_service_port"))
    prefix_url = host + ":" + str(port)

    endpoints_chart = config.get("AppSection", "endpoints_chart").split(",")
    data_charts = [ChartBuilder(prefix_url + endpoint).get_data() for endpoint in endpoints_chart]
    logger.info("Get data charts DONE")

    endpoints_indicators = config.get("AppSection", "endpoints_indicators").split(",")
    data_indicators = [IndicatorBuilder(prefix_url + endpoint).get_data() for endpoint in endpoints_indicators]
    logger.info("Get data indicators DONE")

    data = {"data_charts": data_charts, "data_indicators": data_indicators}

    # 2. Build message
    template_file_path = path.join(path.dirname(path.abspath(__file__)), "template_mail/template_report.html")
    msg_builder = MessageBuilder(template_file_path)
    msg_html = msg_builder.build_message(data)
    logger.info("Build message html from template DONE")

    # 3. Send email
    smtp_host = config.get("SMTPSection", "smtp_host")
    smtp_port = config.get("SMTPSection", "smtp_port")
    sender_email = config.get("SMTPSection", "email_sender")
    receiver_email = config.get("SMTPSection", "email_receiver")
    is_secure_mode = bool(strtobool(config.get("SMTPSection", "is_secure_mode")))
    secure_mode_login = config.get("SMTPSection", "secure_mode_login")
    secure_mode_pwd = config.get("SMTPSection", "secure_mode_pwd")

    # some arguments in env mode
    sender_email = os.getenv("email_sender", sender_email)
    receiver_email = os.getenv("email_receiver", receiver_email)
    secure_mode_login = os.getenv("secure_mode_login", secure_mode_login)
    secure_mode_pwd = os.getenv("secure_mode_pwd", secure_mode_pwd)
 
    email_builder = EmailBuilder(smtp_host, int(smtp_port), sender_email, receiver_email,
                                 is_secure_mode, secure_mode_login, secure_mode_pwd)
    data_img = [data['content'] for data in data_charts if 'error_msg' not in data]
    email_builder.send_email(msg_html, data_img)

    logger.info("Send email DONE")
