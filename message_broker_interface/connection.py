"""
    @Author : Manouchehr Rasouli
    @Date   : 28/June/2018
"""
import stomp
import config_loader
from logger.logging import logger


class Connection:

    def __init__(self):
        pass

    def get_connection(self, config_file="monit_engine.yml"):
        """
        Create and return a stomp connection into
        wanted host message broker.
        :return:
        """
        loader = config_loader.ConfigLoader()
        configuration = loader.get_config()

        logger("INFO", "message_broker_interface/connection : start to connecting to JMS")

        logger("INFO", "message_broker_interface/connection : jms server host : " +
               configuration["monitor_engine.message_server"]["host"])

        logger("INFO", "message_broker_interface/connection : jms server port : " +
               str(configuration["monitor_engine.message_server"]["port"]))

        connection = stomp.Connection([(configuration["monitor_engine.message_server"]["host"],
                                        configuration["monitor_engine.message_server"]["port"])])
        connection.start()

        connection.connect(configuration["monitor_engine.message_server"]["user_name"],
                           configuration["monitor_engine.message_server"]["password"],
                           wait=True)

        # Don't subscribe into any queue just return connection itself.
        return connection
