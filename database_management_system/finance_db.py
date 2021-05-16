"""
    @Author : Manouchehr Rasouli
    @Date   : 14/july/2018
"""
import config_loader
from logger.logging import logger
from logger import date_time


class FinanceDatabase:

    def __init__(self, connection, config_file="monit_engine.yml"):
        """
            finance database
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()
        # select the correct database
        self.database = connection[self.configuration["monitor_engine.data_base"]["database_name"]]
        self.collection = self.database[self.configuration["monitor_engine.data_base"]["finance_collection"]]

        logger("INFO", "database_management_system/finance_db : finance database has initialized")

    def enter_credit(self, credit_dictionary):
        """
            define credit for the user id
        :param credit_dictionary:
        :return:
        """
        credit_dictionary["date"] = date_time.get_date()
        credit_dictionary["user_id"] = str(credit_dictionary["user_id"])
        if not self.check_credit_exists(credit_dictionary["user_id"]):
            self.collection.insert_one({"credit": credit_dictionary})
            return {"status": True, "msg": "credit added successfully"}
        else:
            return {"status": False, "msg": "you must update your credit"}

    def update_credit(self, credit_dictionary):
        """
            this method will update the credit status of the user
        :param credit_dictionary:
        :return:
        """
        self.collection.update({"credit.user_id": credit_dictionary["user_id"]},
                               {"$set": {"credit.requested_finance": credit_dictionary["requested_finance"],
                                         "credit.credit_time": credit_dictionary["credit_time"],
                                         "credit.date": date_time.get_date()}})
        return True

    def check_credit_exists(self, user_id):
        """
            this method will check that the user already have
            credit in our system or not
        :param user_id:
        :return:
        """
        for item in self.collection.find({"credit.user_id": user_id}):
            return True
        return False

    def get_financial_state(self, user_id):
        """
            this function will return the credit state of the user
        :param user_id:
        :return:
        """
        for item in self.collection.find({"credit.user_id": user_id}):
            return item["credit"]["requested_finance"]

    def get_credit_value(self, user_id):
        """
            this method will return the current state of the user
        :param user_id:
        :return:
        """
        for item in self.collection.find({"credit.user_id": user_id}):
            return item["credit"]

    def check_user_credit(self, user_id, finance_config_file="finance_config.yml"):
        """
            check user have credit to
            start to check url database to url add constrain
        :param user_id:
        :return:
        """
        state = self.collection.find({"credit.user_id": user_id})
        loader = config_loader.ConfigLoader(finance_config_file)
        configuration = loader.get_config()
        pass

    def decrease_credit_time(self):
        """
            this method created for decreasing the credit time for each item in database
        :return:
        """
        for item in self.collection.find({}):
            if item["credit"]["requested_finance"] != "free":
                if int(item["credit"]["credit_time"]) > 0:
                    item["credit"]["credit_time"] = str(int(item["credit"]["credit_time"]) - 1)
                    self.collection.update({"credit.user_id": item["credit"]["user_id"]},
                                           {"$set": {"credit.credit_time": item["credit"]["credit_time"]}})
                else:
                    item["credit"]["credit_time"] = "0"
                    self.collection.update({"credit.user_id": item["credit"]["user_id"]},
                                           {"$set": {"credit.credit_time": item["credit"]["credit_time"]}})
        return True

    def get_credits(self):
        """
            this method will return the credits list
        :return:
        """
        credit = []
        for item in self.collection.find({}):
            credit.append(item["credit"])
        return credit
