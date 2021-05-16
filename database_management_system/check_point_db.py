"""
    @Author : Manouchehr Rasouli
    @Date   : 5/july/2018
"""
import config_loader
from logger.logging import logger


class CheckPointDatabase:

    def __init__(self, connection, config_file="monit_engine.yml"):
        """

        :param connection:
        :param config_file:
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()

        # select the correct database
        self.database = connection[self.configuration["monitor_engine.data_base"]["database_name"]]
        self.collection = self.database[self.configuration["monitor_engine.data_base"]["check_point_collection"]]

        logger("INFO", "database_management_system/check_point_db : check point database has initialized")

    def insert_check_point(self, check_point_dictionary):
        """
        :param check_point_dictionary:
        :return:
        """
        value = -1
        if self.check_check_point_not_exist(check_point_dictionary):
            value = self.collection.insert_one({"check_point": check_point_dictionary}).inserted_id
        else:
            pass
        return value

    def get_check_point_info_with_location(self, check_point_location):
        """
            this method will return the check point queue
            with check point location
        :param check_point_location:
        :return:
        """
        data = self.collection.find({"check_point.location": check_point_location})
        for item in data:
            return item["check_point"]
        return False

    def check_check_point_not_exist(self, check_point_dictionary):
        """
            return false if not exist this check point
            elsewhere return true for check point
        :param check_point_dictionary:
        :return:
        """
        cursor = self.collection.find({"check_point.id": check_point_dictionary["id"]})
        for itme in cursor:
            return False
        return True

    def get_all_check_points(self):
        """
            return a list of all of the check points that exists
        :return:
        """
        check_points = []
        cursor = self.collection.find({})
        for item in cursor:
            check_points.append(item["check_point"])
        return check_points
