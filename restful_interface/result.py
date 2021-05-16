"""
    @Author : Manoucher Rasouli
    @Date   : 11/july/2018
"""
from flask_restful import Resource
from flask import request
import json
from result_service import result_service


class Result(Resource):

    def __init__(self, **kwargs):
        """
            created for confirm user info
        :param kwargs:
        """
        self.configuration = kwargs["config_file"]
        self.result_service = result_service.ResultService()

    def put(self):
        """
            put request
        :return:
        """
        return "use get"

    def get(self):
        """
            get request
        :return:
        """
        try:
            result_request = request.data
            if type(result_request) is bytes:
                result_request = result_request.decode('utf-8')
            result_request_dictionary = json.loads(result_request)
            result = self.result_service.get_results(result_request_dictionary)
            return {"result": result, "status": True}
        except Exception as e:
            return {"result": str(e), "status": False}
