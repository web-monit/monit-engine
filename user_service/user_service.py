"""
    @author : Manouchehr Rasouli
"""
import uuid
import config_loader
from schema import validator
from database_management_system import database_connection_pool, user_db
from mail_agent import mailing


class UserService:

    def __init__(self):
        """
        """
        loader = config_loader.ConfigLoader()
        self.configuration = loader.get_config()
        loader = config_loader.ConfigLoader(self.configuration['options_file'])
        self.finance_configuration = loader.get_config()

        self.connection_pool = database_connection_pool.ConnectionPool()
        connection = self.connection_pool.get_connection(self.configuration)
        self.user_database = user_db.UserDatabase(connection)
        self.mail_agent = mailing.Mailing()

    def register_user(self, new_user_dictionary):
        """
        :param new_user_dictionary:
        :return:
        """
        validate = validator.SchemaValidator(self.configuration['schema']['user_register_schema'])
        validate.check(new_user_dictionary)
        new_user_dictionary["user_id"] = uuid.uuid4().hex[0:20]
        new_user_dictionary["is_valid"] = "no"
        new_user_dictionary["confirm_code"] = uuid.uuid4().hex[0:20]
        # create user with free plan
        new_user_dictionary["plan"] = "free"
        new_user_dictionary["credit"] = self.finance_configuration[new_user_dictionary["plan"]]
        # Generate a email confirm code and send into the user email address
        result = self.user_database.check_user(new_user_dictionary)
        if result["status"] is True:
            mail_info = {
                "to": new_user_dictionary["email_address"],
                "subject": "confirm code",
                "msg": "your confirm code is -- " + str(new_user_dictionary["confirm_code"])
            }
            result["msg"] = "the confirm code has sent !"
            # todo : mail agent have some problems in sending email
            # self.mail_agent.send(title=mail_info['subject'], message=mail_info['msg'], to=mail_info['to'])
            # create user in database
            self.user_database.insert_user(new_user_dictionary)
        else:
            raise Exception("an error during create the user ")

        return new_user_dictionary['user_id']

    def confirm_user(self, confirm_dictionary):
        """
        :param confirm_dictionary:
        :return:
        """
        validate = validator.SchemaValidator(self.configuration['schema']['user_register_confirm_schema'])
        validate.check(confirm_dictionary)
        return self.user_database.confirm_user(confirm_dictionary["user_id"],
                                               confirm_dictionary["confirm_code"])

    def authorize_user(self, authentication_dictionary):
        """
        :param authentication_dictionary:
        :return:
        """
        validate = validator.SchemaValidator(self.configuration['schema']['user_authentication_schema'])
        validate.check(authentication_dictionary)
        return self.user_database.check_user_password(authentication_dictionary["user_name"],
                                                      authentication_dictionary["password"])

    def get_user_info(self):
        raise Exception('not implemented')

    def get_user_credit(self, user_id):
        """
        :param user_id:
        :return:
        """
        return self.user_database.get_user_credit(user_id=user_id)
