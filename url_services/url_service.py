"""

        @author : Manouchehr Rasouli

"""
from user_service import user_service
from check_point_service import check_point_service
from schema import validator
import config_loader
from database_management_system import database_connection_pool, url_db
import uuid
from message_broker_interface_sender import send_module


class UrlService:

    def __init__(self):
        """
            this class created to manage and handle the url actions
        """
        loader = config_loader.ConfigLoader()
        self.config = loader.get_config()
        self.user_service = user_service.UserService()
        self.check_point_service = check_point_service.CheckPointService()
        self.sender = send_module.SendModule()

        connection_pool = database_connection_pool.ConnectionPool()
        db_connection = connection_pool.get_connection(self.config)
        self.url_database = url_db.UrlDatabase(db_connection)

    def subscribe_url(self, info):
        """
            this function will subscribe the new info into the system
        :param self:
        :param info:
        :return:
        """

        # todo : add confirm url content for user ...
        # todo : have to load url once and show content to user
        # todo : to version-ing reasons

        validate = validator.SchemaValidator(self.config['schema']['url_register_schema'])
        validate.check(info)
        info["credit"] = self.user_service.get_user_credit(info["user_id"])
        # external info for new url
        info["url_id"] = uuid.uuid4().hex[0:20]
        info["is_valid"] = "yes"
        # the action will describe the correct activity in check point
        info["action"] = "add"

        url_count = len(self.get_urls({"user_id": info["user_id"]}))
        if url_count > info["credit"]["maximum_url"]:
            raise Exception("maximum url constraint has reached")
        for location in info["credit"]["url_check_locations"]:
            check_point = self.check_point_service.get_check_point_info_with_location(location)
            self.sender.send(destination=check_point["queue"], message=info)
        self.url_database.insert_url(info)
        return "url subscribed successfully"

    def get_urls(self, requested_url_dic):
        """
        :param requested_url_dic:
        :return:
        """
        validate = validator.SchemaValidator(self.config['schema']['url_fetch_schema'])
        validate.check(requested_url_dic)
        return self.url_database.get_url_for(requested_url_dic["user_id"])

    def update_url(self, info):
        """

            we don't need to update urls

        :param info:
        :return:
        """
        raise NotImplementedError

    def delete_url(self, info):
        """

            update url as invalid

        :param info:
        :return:
        """
        validate = validator.SchemaValidator(self.config['schema']['url_delete_schema'])
        validate.check(info)
        info["action"] = "delete"

        url = self.url_database.get_url(info['url_id'])
        # send into check points
        for location in url["credit"]["url_check_locations"]:
            check_point = self.check_point_service.get_check_point_info_with_location(location)
            self.sender.send(destination=check_point["queue"], message=info)
        self.url_database.delete_url(info['url_id'])
        return "url deleted successfully"
