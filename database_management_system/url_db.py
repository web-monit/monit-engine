"""
    @Author : Manouchehr Rasouli
    @Date   : 8/july/2018
"""
import config_loader
from logger.logging import logger


class UrlDatabase:

    def __init__(self, connection, config_file="monit_engine.yml"):
        """
            pass
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()

        # select the correct database
        self.database = connection[self.configuration["monitor_engine.data_base"]["database_name"]]
        self.collection = self.database[self.configuration["monitor_engine.data_base"]["url_collection"]]

        logger("INFO", "database_management_system/url_db : url database has initialized")

    def insert_url(self, url_dic):
        """
            start to inserting the url dictionary
        :param url_dic:
        :return:
        """
        self.collection.insert_one({"url": url_dic})
        return

    def delete_url(self, url_id):
        """
            delete the url from system
        :param url_dic:
        :return:
        """
        return self.collection.update({"url.url_id": str(url_id)}, {"$set": {"url.is_valid": "no"}})

    def update_url(self, url_dic):
        """
            this method created for do update operation on the urls

            db.your_collection.update({},
                          {$set : {"new_field":1}},
                          {upsert:false,
                          multi:true})

        :param url_dic:
        :return:
        """
        for item in url_dic["fields"]:
            self.collection.update({"url.url_id": url_dic["url_id"]},
                                   {"$set": {"url." + str(item): url_dic["fields"][item]}},
                                   upsert=False, multi=True)
        return True

    def get_url(self, url_id):
        """
            this function will return the url for the requested url_id
        :param url_id:
        :return:
        """
        for item in self.collection.find({"url.url_id": url_id}):
            return item["url"]
        return None

    def get_url_owner(self, url_id):
        """
            this method will return the url owner with url id
        :param url_id:
        :return:
        """
        data_collection = self.collection.fint({"url.url_id": url_id})
        for data in data_collection:
            return data["url"]["url_owner"]
        return None

    def get_location_for(self, url_id):
        """
            return the locations for the url id that requested
        :param url_id:
        :return:
        """
        for item in self.collection.find({"url.url_id": str(url_id)}):
            return item["url"]["url_check_locations"]
        return None

    def get_url_for(self, user_id):
        """
            return the url list for specified url owner id
        :param user_id:
        :return:
        """
        data = self.collection.find({'url.user_id': user_id})
        urls = []
        for item in data:
            if item['url']['is_valid'] == 'yes':
                urls.append(item['url'])
        return urls

    def get_url_for_location(self, location):
        """
            return urls for location
        :param location:
        :return:
        """
        pass

    def get_urls(self):
        """
            return urls that stored in database
        :return:
        """
        url = []
        data = self.collection.find({})
        for item in data:
            item["_id"] = "----"
            url.append(item)
        return url

    def generate_id(self):
        """
            this method will generate a url id for new arrived url
        :return:
        """
        count = 0
        data = self.collection.find({})
        for item in data:
            count = count + 1
        return count

    def get_number_of_urls(self, user_id):
        """
            this method will return the number of urls that this user registered im our system
        :param user_id:
        :return:
        """
        count = 0
        for item in self.collection.find({"url.url_owner": user_id}):
            if item["url"]["is_valid"] == "yes":
                count = count + 1
        return count
