"""
    @Author : Manouchehr Rasouli
    @Date   : 5/july/2018

    service starter created for handle and start all of services that
    monitor engine works on it.
"""
from logger.logging import logger
from message_broker_interface import connection as message_broker_connection
from message_broker_interface import connection_handler as message_broker_connection_handler
from message_broker_interface_listener import registration_listener, result_listener
import config_loader


class StarterKit:

    def __init__(self):
        """
            initial starter kit
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()

        logger("INFO", "service_starter : start starter kit to initialization")

        # start all of the services
        self.__start_all__()

        logger("INFO", "service_starter : starter service has completed initialization")

    def __start_all__(self):
        """
            start all of the system services
        :return:
        """
        # message broker connection manager
        broker_connection_manager = message_broker_connection.Connection()

        # initialize registration connection handler
        registry_connection = broker_connection_manager.get_connection()
        message_broker_connection_handler.Handler(connection=registry_connection,
                                                  connection_listener=registration_listener,
                                                  topic=
                                                  self.configuration["monitor_engine.message_server"]["subscription"][
                                                      0])

        # initialize result connection handler
        result_connection = broker_connection_manager.get_connection()
        message_broker_connection_handler.Handler(connection=result_connection,
                                                  connection_listener=result_listener,
                                                  topic=
                                                  self.configuration["monitor_engine.message_server"]["subscription"][
                                                      1])
