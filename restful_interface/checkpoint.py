"""
    @Author : Manouchehr Rasouli
    @Date   : 10/july/2018
"""
from flask_restful import Resource
import json
from flask_jwt_extended import jwt_required
from check_point_service import check_point_service


class CheckPoint(Resource):

    def __init__(self, **kwargs):
        """
            url request must be in this format

            url = {"the request"}
        """
        self.configuration = kwargs["config_file"]
        self.check_point_service = check_point_service.CheckPointService()

    @jwt_required
    def get(self):
        """
            the get request handler
        :return:
        """
        try:
            data = self.check_point_service.get_check_points_list()
            return json.dumps({"result": data, "status": True})
        except Exception as e:
            return json.dumps({"result": str(e), "status": False})

    @jwt_required
    def put(self):
        """
            pass
        :return:
        """
        return "use get"
