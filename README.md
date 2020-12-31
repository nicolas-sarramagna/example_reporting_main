# Example of usages of python consume API, html email with images and unittest

![screeen_email](https://github.com/nicolas-sarramagna/example_reporting_main/blob/main/images/screen_email.png)

## Daily email report of the market Bitcoin - USD

## Local :
1. start a local smtp server : docker run -p 1080:80 -p 1025:25 maildev/maildev
2. start web services server from https://github.com/nicolas-sarramagna/example_reporting_web_services
3. export PYTHONPATH=.

python example_reporting_main/main.py

The main function consumes the endpoints of the api server, creates the html message and send the email.

## Docker : in progress

## Online : in progress
