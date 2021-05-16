"""
    @Author : Manouchehr Rasouli
    @Date   : 28/June/2018
"""
import config_loader
import time
import threading
from logger.logging import logger


class Handler:

    def __init__(self, connection, connection_listener, topic, config_file="monit_engine.yml"):
        loader = config_loader.ConfigLoader()
        configuration = loader.get_config()

        self.connection = connection

        self.connection.set_listener("message_broker_interface_listener", connection_listener.Listener())

        self.connection.subscribe(destination=topic,
                                  id=configuration["monitor_engine.message_server"]["id"],
                                  ack='auto')

        logger("INFO", "message_broker/connection_handler : connection stablished successfully for topic : " + topic)

        thread = threading.Thread(target=self.__run__, args=())
        thread.daemon = True
        thread.start()

    def __run__(self):
        """ Method that runs forever """
        while True:
            time.sleep(1)


