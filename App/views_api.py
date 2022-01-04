from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import json
from django.core import serializers

from .models_main import Country

from .services_api import *
from .decorators_views import check_api_key

@api_view(['GET'])
def get_all_default_countries(_):
    """
 	Return all default countries
 	"""
    json_countries = serializers.serialize("json", Country.objects.all())

    if json_countries:
        orm_countries = json.loads(json_countries)
        countries = list(map(change_keys_to_values, orm_countries))
        data = json.dumps(countries)
        return Response(data, status=status.HTTP_201_CREATED)
    return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@check_api_key
def get_saved_games_of_user(request):
    """
    Get all saves of user with authorization
    """
    if not request.user.is_authenticated:
        req_data = request.data
        login_status = login_with_request_data(request, req_data)
        if not login_status:
            return Response(json.dumps({
                'saves': 'error',
            }), status=status.HTTP_401_UNAUTHORIZED)

    json_saves = serializers.serialize("json", list(request.user.saves.all()))
    dict_saves = json.loads(json_saves)
    json_saves = list(map(set_name_of_saved_game, dict_saves))
    data = json.dumps(json_saves)
    
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@check_api_key
def delete_save_by_time(request):
    """
    Delete save by data from request
    """
    req_data = request.data
    user = get_user_by_name(req_data['login'])
    save = get_save_by_save_time(user, req_data)

    if not (user and save):
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    user = delete_save_by_object(user, save)

    all_saves = serializers.serialize("json", list(user.saves.all()))
    dict_all_saves = json.loads(all_saves)
    all_saves = list(map(set_name_of_saved_game, dict_all_saves))
    data = json.dumps(all_saves)

    return Response(data, status=status.HTTP_201_CREATED)