from rest_framework import renderers
from json import dumps

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, amt=None, context=None):
        if 'Msg' in str(data):
            response = dumps({'Data':data})
        else:
            response = dumps({'Errors':data})
        return response