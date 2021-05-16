"""
    @author : Manouchehr Rasouli
"""
from email.mime.text import MIMEText
import smtplib
from logger.logging import logger
from config_loader import ConfigLoader


class Mailing:

    def __init__(self):
        """
            the loaded config file will pass into this class
        :param config:
        """
        loader = ConfigLoader()
        self.config = loader.get_config()
        self.smtp_ssl_host = self.config["mail_service.mail_host"]["email_host"][0]
        self.smtp_ssl_port = self.config["mail_service.mail_host"]["email_port"]
        self.username = self.config["mail_service.mail_host"]["email_user_name"]
        self.password = self.config["mail_service.mail_host"]["email_host_password"]
        self.sender = self.config["mail_service.mail_host"]["email_user_name"]

    def send(self, title, message, to):
        """
        :param title:
        :param message:
        :param to:
        :return:
        """
        logger("INFO", "mail_agent/mailing : start sending email to : " + to)
        targets = [to]

        msg = MIMEText(message, )
        msg['Subject'] = title
        msg['From'] = self.sender
        msg['To'] = ', '.join(targets)

        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        server.login(self.username, self.password)
        server.sendmail(self.sender, targets, msg.as_string())
        server.quit()
        logger("INFO", "mail_agent/mailing : email sent successfully")
