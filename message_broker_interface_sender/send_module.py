"""
    @author : Manouchehr Rasouli

        this module created for sending message over
        messaging system.
"""
from message_broker_interface import connection
import json


class SendModule:

    def __init__(self):
        connector = connection.Connection()
        self.general_connection = connector.get_connection()

    def send(self, destination, message):
        """
        :param destination:
        :param message:
        :return:
        """
        if type(message) is dict:
            self.general_connection.send(destination=destination, body=json.dumps(message))
        else:
            self.general_connection.send(destination=destination, body=message)
