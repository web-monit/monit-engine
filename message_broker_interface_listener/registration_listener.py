"""
    @Author : Manouchehr Rasouli
    @Date   : 28/June/2018
"""
import stomp
from logger.logging import logger
from check_point_service import check_point_service
import json


class Listener(stomp.ConnectionListener):

    def __init__(self):
        logger("INFO",
               "message_broker_interface_listener/registration_listener : listener established")
        self.checkpoint_handler = check_point_service.CheckPointService()

    def on_error(self, headers, message):
        # Do some operation on the error message !
        logger("ERROR", "message_broker_interface_listener/registration_listener : " + message)

    def on_message(self, headers, message):
        try:
            logger("INFO", "message_broker_interface_listener/registration_listener : register requests")
            if type(message) is bytes:
                message = message.data.decode('utf-8')
            message_dic = json.loads(message)
            self.checkpoint_handler.add_check_point(message_dic)
        except Exception as e:
            logger("EXCEPTION", "message_broker_interface_listener/registration_listener : " + str(e))
