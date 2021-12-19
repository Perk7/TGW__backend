from django.db import transaction

from rest_framework.decorators import api_view
import json

from rest_framework.response import Response
from rest_framework import status

from .services_game import *

@api_view(['POST'])
@transaction.atomic
def start_game(request):
    """
    Get user with selected country and make new game
    """
    data = request.data

    new_game = create_new_game(data['user'], data['country'])
    
    data = json.dumps(new_game.as_json())

    return Response(data, status=status.HTTP_201_CREATED if new_game else status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def load_game(request):
    """
    Load having game by time
    """
    data = request.data
    
    save = load_game_by_time(data['user'], data['time'])

    data = json.dumps(save.as_json())

    return Response(data, status=status.HTTP_201_CREATED if save else status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@transaction.atomic
def save_game(request):
    """
    Save having game
    """
    data = request.data
    
    save = save_current_game(data['username'], data['store'])

    data = json.dumps(save.as_json())

    return Response(data, status=status.HTTP_201_CREATED if save else status.HTTP_204_NO_CONTENT)
