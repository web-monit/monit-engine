"""
    @author : Manouchehr Rasouli

        this service created for manage and
        deal with results that gathered with
        check points.
"""
from database_management_system import database_connection_pool, result_db
import config_loader


class ResultService:

    def __init__(self):
        """
        """
        loader = config_loader.ConfigLoader()
        connection_pool = database_connection_pool.ConnectionPool()
        connection = connection_pool.get_connection(configuration=loader.get_config())
        self.db = result_db.ResultDatabase(connection=connection)

    def add_result(self, info):
        print(info)
        if info['result']['up_and_speed']['status'] is not True:
            # todo : send email and content of the page
            pass
        else:
            # todo : content check for url to find any change
            # todo : push data for use that online
            # todo : implement the django pusher
            self.db.insert_result(info)

    def get_results(self, info):
        raise NotImplementedError
