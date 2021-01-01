# Example of usages of python consume API, html email with images and unittest

## Daily email report of the market Bitcoin - USD

![screeen_email](https://github.com/nicolas-sarramagna/example_reporting_main/blob/main/images/screen_email.png)

## Local dev mode :
1. start a local smtp server, in a terminal, type **docker run -p 1080:80 -p 1025:25 maildev/maildev**
2. start the web services server, see https://github.com/nicolas-sarramagna/example_reporting_web_services
3. from the source code, 
  - in a terminal, type **export PYTHONPATH=.;python example_reporting_main/main.py**
  
  See the file [config.cfg](https://github.com/nicolas-sarramagna/example_reporting_main/blob/main/example_reporting_main/config/config.cfg) for the configuration of the smtp server (smtp gmail for example) to send the mail in a real mailblox.
  
or
  - with docker, type **docker-compose up**
  
  See the folder [docker_config_dev](https://github.com/nicolas-sarramagna/example_reporting_main/tree/main/docker_config_dev) for the configuration files (config.cfg and logging.cfg)
  
The main function consumes the endpoints of the api server, creates the html message and sends the email.

So, by default, the email is visible on the maildev webmail on http://localhost:1080 

## Prod mode (example with smtp gmail) : 
Complete and export the variables var_email_sender, var_email_receiver, var_secure_mode_login, var_secure_mode_pwd.
**export var_email_sender= ; export var_email_receiver= ; export var_secure_mode_login= ; export var_secure_mode_pwd= ;**

and type

**type docker-compose -f prod_env.yml**

See the folder [docker_config_prod](https://github.com/nicolas-sarramagna/example_reporting_main/tree/main/docker_config_prod) for the configuration files (config.cfg and logging.cfg)

## Online mode : daily report with circleci
CircleCI does not support the Docker volumes natively (see this [link](https://support.circleci.com/hc/en-us/articles/360007324514-How-can-I-use-Docker-volume-mounting-on-CircleCI-) for ex).

Here,i use a workaround to call the the prod folder in the main function with an optional enviromnent variable.

The circle ci config file [config.yml](https://github.com/nicolas-sarramagna/example_reporting_main/blob/main/.circleci/config.yml)  
