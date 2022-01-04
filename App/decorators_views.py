import hashlib
from django.db.models.query import RawQuerySet

from rest_framework.response import Response
from .models_auth import CustomAuth
from dotenv import dotenv_values

import json
from rest_framework import status

from typing import Callable

config = dotenv_values(".env") 

def check_api_key(func: Callable) -> Callable:
    """
    Check the valid secret api key for rest api requests
    """
    def wrapped_check_function(request) -> Response:
        if all([i in request.data.keys() for i in ['key', 'code', 'login']]):
            key, code, login = request.data['key'], request.data['code'], request.data['login']
        else:
            return Response(json.dumps({
                    'status': False,
                    'desc': "Bad request"
                }), status=status.HTTP_400_BAD_REQUEST)

        reversed_login = login[::-1]
        if login not in [i.username for i in CustomAuth.objects.all()]:
            return Response(json.dumps({
                    'status': False,
                    'desc': "You are not authorizied"
                }), status=status.HTTP_401_UNAUTHORIZED)
    
        secret_key = config['SECRET_KEY']

        str_for_hash = secret_key + ':' +  reversed_login + ':' + code 

        hash_object = hashlib.sha256(bytes(str_for_hash, encoding='utf-8'))
        hex_enc = hash_object.hexdigest()
        
        if key != hex_enc:
            return Response(json.dumps({
                    'status': False,
                    'desc': "You are not authorizied"
                }), status=status.HTTP_401_UNAUTHORIZED)
        else:
            result = func(request)
            return result
    return wrapped_check_function
