"""
    @author : Manouchehr Rasouli
"""
from config_loader import ConfigLoader
from database_management_system import database_connection_pool, check_point_db
from schema import validator
from logger.logging import logger


class CheckPointService:

    def __init__(self):
        """
            this class created for handling and dealing with check points
        """
        config_loader = ConfigLoader()
        self.config = config_loader.get_config()
        connection_pool = database_connection_pool.ConnectionPool()
        connection = connection_pool.get_connection(self.config)
        self.database = check_point_db.CheckPointDatabase(connection=connection)

    def add_check_point(self, info):
        """
        :param info: type json
        :return:
        """
        validate = validator.SchemaValidator(self.config['schema']['checkpoint_register_schema'])
        validate.check(info)
        self.database.insert_check_point(info)
        logger("INFO",
               "check_point_service/check_point_service/add_check_point : check point has initialized successfully")
        return {'status': True, 'result': 'check point registered successfully'}

    def get_check_points_list(self):
        """
            this function will return the info of the check points
        :return:
        """
        return self.database.get_all_check_points()

    def get_check_point_info_with_location(self, check_point_location):
        """
            this function will return all of the information about the check point itself
        :param check_point_location:
        :return:
        """
        return self.database.get_check_point_info_with_location(check_point_location=check_point_location)
