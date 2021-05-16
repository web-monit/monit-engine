"""
    @author : Manouchehr Rasouli
"""


class SMSAgent:

    def __init__(self, config):
        """
            the loaded config file will pass into this class
        :param config:
        """
        self.config = config

    def send(self, message, to):
        """
        :param message:
        :param to:
        :return:
        """
        raise Exception('not implemented')
