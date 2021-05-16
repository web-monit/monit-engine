"""
    @Author : Manouchehr Rasouli
    @Date   : 8/july/2018


    this module created for a restful interface for work with urls
"""
from flask_restful import Resource
from flask import request
import json
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from user_service import user_service
from datetime import timedelta
from logger.logging import logger


class UserRegistry(Resource):

    def __init__(self, **kwargs):
        """
            url request must be in this format

            url = {"the request"}

        """
        self.configuration = kwargs["config_file"]
        self.user_service = user_service.UserService()

    def get(self):
        """
            the get request handler
        :return:
        """
        return "use put"

    def put(self):
        """
            the put request handler
        :return:
        """
        try:
            result = {}
            new_user = request.data
            if type(new_user) is bytes:
                new_user = new_user.decode("utf-8")
            new_user_dictionary = json.loads(new_user)
            result['user_id'] = self.user_service.register_user(new_user_dictionary)
            status = True
        except Exception as e:
            status = False
            result = str(e)
            logger("EXCEPTION", "restful_interface/user/user_register : " + str(e))
        return {"result": result, "status": status}


class ConfirmUserAuthentication(Resource):

    def __init__(self, **kwargs):
        """
            created for confirm user info
        :param kwargs:
        """
        self.configuration = kwargs["config_file"]
        self.user_service = user_service.UserService()

    def put(self):
        """
            put request
        :return:
        """
        try:
            confirmation = request.data
            if type(confirmation) is bytes:
                confirmation = confirmation.decode("utf-8")
            confirm_dictionary = json.loads(confirmation)
            result = self.user_service.confirm_user(confirm_dictionary)
            return {"result": result, "status": True}
        except Exception as e:
            return {"result": str(e), "status": False}

    def get(self):
        """
            get request
        :return:
        """
        return "use put"


class UserAuthentication(Resource):

    def __init__(self, **kwargs):
        """
            used for user authentication and log in action on outer layer
        :param kwargs:
        :return:
        """
        self.configuration = kwargs["config_file"]
        self.blacklist = kwargs["blacklist"]
        self.user_service = user_service.UserService()

    @jwt_required
    def get(self):
        """
            use get request to check out the property and information of the user with stored
            jwt.
        :return:
        """
        return {'status': True, 'authenticated': get_jwt_identity()}

    @jwt_required
    def post(self):
        """
            the delete function created for log out
        :return:
        """
        print('test')
        jti = get_raw_jwt()['jti']
        self.blacklist.add(jti)
        return {'status': True, 'msg': 'user logout successfully'}

    def put(self):
        """
            pass
        :return:
        """
        try:
            authentication_request = request.data
            if type(authentication_request) is bytes:
                authentication_request = authentication_request.decode('utf-8')
            authentication_request_dictionary = json.loads(authentication_request)
            result = self.user_service.authorize_user(authentication_request_dictionary)
            # create access token if authentication vent well
            if result["result"]:
                result["access_token"] = create_access_token(
                    identity={'user': authentication_request_dictionary["user_name"], 'user_id': result['user_id']},
                    fresh=True,
                    expires_delta=timedelta(seconds=self.configuration["monitor_engine.property"]["jwt_expire_delta"]))
            return {"result": result, "status": True}
        except Exception as e:
            return {"result": str(e), "status": False}
