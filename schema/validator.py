"""
    @author : Manouchehr Rasouli
"""
from jsonschema import validate
import json


class SchemaValidator:

    def __init__(self, schema_path):
        """
        :param schema_path:
        """
        file = open(schema_path, 'r').readlines()
        schema = ""
        for line in file:
            schema = schema + line
        self.schema = json.loads(schema)

    def check(self, data):
        """
        :param data:
        :return:
        """
        return validate(data, schema=self.schema)
