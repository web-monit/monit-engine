"""
    @author : Manouchehr Rasouli
"""
import yaml


class ConfigLoader:

    def __init__(self, config="monit_engine.yml"):
        """
        :param config_path:
        """
        self.config_path = config
        file = open(self.config_path, 'r')
        self.config = yaml.load(file, yaml.FullLoader)

    def get_config(self):
        """
        :return:
        """
        return self.config
