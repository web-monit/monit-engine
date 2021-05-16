"""
    @Author : Manouchehr Rasouli
    @Date   : 8/july/2018


    this module created for a restful interface for work with urls
"""
from flask_restful import Resource
from flask import request
import json
from flask_jwt_extended import jwt_required
from url_services import url_service


class UrlRegister(Resource):

    def __init__(self, **kwargs):
        """
            url request must be in this format

            url = {"the request"}

        """
        self.configuration = kwargs["config_file"]
        self.url_service = url_service.UrlService()

    @jwt_required
    def get(self):
        """
            the get request handler
        :return:
        """
        return "use put"

    @jwt_required
    def put(self):
        """
            the put request handler
        :return:
        """
        try:
            new_url = request.data
            if type(new_url) is bytes:
                new_url = new_url.decode('utf-8')
            new_url_dictionary = json.loads(new_url)
            result = self.url_service.subscribe_url(new_url_dictionary)
            return {"status": True, "result": result}
        except Exception as e:
            return {"result": str(e), 'status': False}


class GetUrl(Resource):

    def __init__(self, **kwargs):
        """
            This class created for returning the url list for the user id that we request
        """
        self.configuration = kwargs["config_file"]
        self.url_service = url_service.UrlService()

    @jwt_required
    def get(self):
        """
            this method created for returning the urls for a url owner
        :return:
        """
        try:
            requested_url = request.data
            if type(requested_url) is bytes:
                requested_url = requested_url.decode('utf-8')
            requested_url_dic = json.loads(requested_url)
            result = self.url_service.get_urls(requested_url_dic)
            return {"result": result, "status": True}
        except Exception as e:
            return {"result": str(e), "status": False}

    @jwt_required
    def put(self):
        """
            pass
        :return:
        """
        return "use get"


class DeleteUrl(Resource):

    def __init__(self, **kwargs):
        """
            pass arguments to delete url
        :param kwargs:
        """
        self.configuration = kwargs["config_file"]
        self.url_service = url_service.UrlService()

    @jwt_required
    def put(self):
        """
        :return:
        """
        try:
            requested_url = request.data
            if type(requested_url) is bytes:
                requested_url = requested_url.decode('utf-8')
            requested_url_dic = json.loads(requested_url)
            result = self.url_service.delete_url(requested_url_dic)
            return {"result": result, "status": True}
        except Exception as e:
            return {"result": str(e), "status": False}
