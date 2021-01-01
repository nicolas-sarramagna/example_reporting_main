# Example of usages of python consume API, html email with images and unittest

## Daily email report of the market Bitcoin - USD

![screeen_email](https://github.com/nicolas-sarramagna/example_reporting_main/blob/main/images/screen_email.png)

## Local :
1. start a local smtp server : docker run -p 1080:80 -p 1025:25 maildev/maildev
2. start web services server from https://github.com/nicolas-sarramagna/example_reporting_web_services
3. export PYTHONPATH=.

python example_reporting_main/main.py

The main function consumes the endpoints of the api server, creates the html message and send the email.

## Docker : 

Local docker-compose up
Email

config.cfg 

export var_email_sender=
export var_email_receiver=
export var_secure_mode_login=
export var_secure_mode_pwd=



## Online : in progress via circleci
