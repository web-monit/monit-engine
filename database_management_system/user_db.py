"""
    @Author : Manoucher Rasouli
    @Date   : 10/july/2018
"""
import config_loader
from logger.logging import logger


class UserDatabase:

    def __init__(self, connection, config_file="monit_engine.yml"):
        """
            pass
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()

        # select the correct database
        self.database = connection[self.configuration["monitor_engine.data_base"]["database_name"]]
        self.collection = self.database[self.configuration["monitor_engine.data_base"]["user_collection"]]

        logger("INFO", "database_management_system/user_db : user database has initialized")

    def insert_user(self, user_dic):
        """
            insert new user into the system
        :param user_dic:
        :return:
        """
        if not self.check_user_name(user_dic["user_name"]):
            if self.check_email_exist(user_dic["email_address"]):
                self.collection.insert_one({"user": user_dic})
                return {"status": True, "user_id": user_dic["user_id"]}
            else:
                return {"status": False, "msg": "email already registered in system :|"}
        else:
            return {"status": False, "msg": "user name exist !"}

    def check_user(self, user_dic):
        """
        :param user_dic:
        :return:
        """
        if not self.check_user_name(user_dic["user_name"]):
            if self.check_email_exist(user_dic["email_address"]):
                return {"status": True, "user_id": user_dic["user_id"]}
            else:
                return {"status": False, "msg": "email already registered in system :|"}
        else:
            return {"status": False, "msg": "user name exist !"}

    def confirm_user(self, user_id, confirm_code):
        """
            this method created for confirmation of the usr
        :param user_id:
        :param confirm_code:
        :return:
        """
        for item in self.collection.find({"user.user_id": user_id}):
            if item["user"]["confirm_code"] == confirm_code:
                self.collection.update({"user.user_id": user_id},
                                       {"$set": {"user.is_valid": "yes"}})
                return {"result": True, "msg": "the code is correct !"}
            else:
                return {"result": False, "msg": "confirm code is not correct !"}
        return {"result": False, "msg": "the user name is not correct !"}

    def check_email_exist(self, email_address):
        """
            this method will check that email is replicated or not
        :param email_address:
        :return:
        """
        for item in self.collection.find({"user.email_address": email_address}):
            if item["user"]["is_valid"] != "no":
                return False
        return True

    def delete_user(self, user_dic):
        """
            to delete the user form system engine
        :param user_dic:
        :return:
        """
        pass

    def check_user_name(self, user_name):
        """
            check user name exists

            false if not exist
            true if exist
        :param user_name:
        :return:
        """
        data = self.collection.find({"user.user_name": user_name})
        for item in data:
            if item["user"]["is_valid"] != "no":
                return True
        return False

    def check_user_password(self, user_name, password):
        """
            check that user password is correct or not
        :param password:
        :param user_name
        :return:
        """
        data = self.collection.find({"user.user_name": user_name})
        for item in data:
            if item["user"]["password"] == password:
                if item["user"]["is_valid"] == "yes":
                    return {"result": True, "user_id": item["user"]["user_id"], "msg": "you are authorized"}
        return {"result": False, "msg": "Invalid username or password !"}

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

    def get_user_info(self, user_id):
        """
            this method will return user information for the user id
        :param user_id:
        :return:
        """
        data_collection = self.collection.find({"user.user_id": str(user_id)})
        for data in data_collection:
            return data["user"]
        return None

    def get_users_email_list(self):
        """
            this method will return all of the valid users that registered in the system
        :return:
        """
        mail_list = []
        for item in self.collection.find({"user.is_valid": "yes"}):
            mail_list.append(item["user"]["email_address"])
        return mail_list

    def get_user_credit(self, user_id):
        """
        :param user_id:
        :return:
        """
        for item in self.collection.find({"user.user_id": user_id}):
            return item["user"]["credit"]
        return None
