from jinja2 import Template
from example_reporting_main.base_logger import logger


class MessageBuilder:
    """
    class to build the message to send in email
    """

    def __init__(self, abspath_filename: str) -> None:
        """
        create self.template from the template html file
        :param abspath_filename:absolute path of the template html file
        """
        logger.debug("Read template file html")
        with open(abspath_filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        logger.debug("Read template file html DONE")
        self.template = Template(template_file_content)

    def build_message(self, data: dict) -> str:
        """
        apply the data on the template
        Warning : the template html must use the variable with prefix data
        ex : <h1>{{data.title_var}</h1> -> my_dict = {'title_var':'title_value'}
        :param data: dict of the variable and value to apply
        :return:the message to send in an email
        """
        message = self.template.render(data=data)
        logger.debug("Build message result :" + message)
        return message
