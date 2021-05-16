"""
    @Author : Manouchehr Rasouli
    @Date   : 5/july/2018
"""
import config_loader
from logger.logging import logger


class ResultDatabase:

    def __init__(self, connection):
        """
            oops
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()

        # select the correct database
        self.database = connection[self.configuration["monitor_engine.data_base"]["database_name"]]
        self.collection = self.database[self.configuration["monitor_engine.data_base"]["result_collection"]]

        logger("INFO", "database_management_system/result_db : result database has initialized")

    def insert_result(self, result_dictionary):
        """
            insert the result into result dictionary
        :return:
        """
        result_id = self.collection.insert_one({"result": result_dictionary}).inserted_id
        return result_id

    def get_all_results(self):
        """
            return all of the results that we have in database
        :return:
        """
        results = []
        data = self.collection.find({})
        for item in data:
            results.append(item['result'])
        return results

    def get_result_for_url(self, url):
        """
            return results for the selected url
        :param url:
        :return:
        """
        pass

    def get_data(self, url_id, from_time, to_time):
        """
            return the results for specified url id
            from data to date :|

    db.result.find( { "result.time": { $gte: "Tue, 10 Jul 2018 06:52:25 +0000", $lt: "Wed, 11 Jul 2018 06:16:28 +0000" }
                                    , "result.url_id":"1" } )

        :param url_id:
        :param from_time:
        :param to_time:
        :return:
        """
        result_list = []
        for item in self.collection.find({"result.time": {"$gte": from_time, "$lt": to_time}, "result.url_id": url_id}):
            result_list.append(item["result"])
        return result_list
