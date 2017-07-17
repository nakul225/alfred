import json 
from step import Step

class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Step) or isinstance(obj, Goal):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)