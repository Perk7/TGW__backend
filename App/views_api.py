from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from django.core import serializers
from django.shortcuts import get_object_or_404
from .models_auth import CustomAuth
from django.contrib.auth.hashers import check_password
from .models_main import Country, Regions, Squad
from .models_saves import SaveCountry
from django.contrib.auth import login

from django.db.utils import OperationalError

from django.db import transaction
import datetime

def change_cap(x):
    cap =  get_object_or_404(Regions, id=x['fields']['capital'])
    coun = get_object_or_404(Country, id=x['pk'])
    army = Squad.objects.filter(country = x['pk'])
    army_col = 0
    for i in army:
        army_col += i.summ()
    govern = x['fields']['government'][0]

    x['fields']['capital'] = cap.capital
    x['fields']['population'] = coun.get_population()
    x['fields']['area'] = coun.get_area()
    x['fields']['gdp'] = coun.get_gdp()
    x['fields']['army'] = army_col
    if govern == 'O':
        x['fields']['government'] = 'Ограниченная монархия'
    elif govern == 'M':
        x['fields']['government'] = 'Абсолютная монархия'
    elif govern == 'D':
        x['fields']['government'] = 'Однопартийная диктатура'
    elif govern == 'R':
        x['fields']['government'] = 'Республика'

    return x

def change_load(x):
    cap = get_object_or_404(SaveCountry, id=x['fields']['country'])
    x['fields']['save_name'] = cap.name
    return x

@api_view(['GET'])
def all_countries(request):
    """
 	Return all Countries
 	"""
    if request.method == 'GET':
        data = serializers.serialize("json", Country.objects.all())
        if data:
            des = json.loads(data)
            new_des = list(map(change_cap, des))
            data = json.dumps(new_des)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def saved_games(request):
    if not request.user.is_authenticated:
        post = request.data
        try:
            if CustomAuth.objects.filter(username=post['login']):
                user = get_object_or_404(CustomAuth, username=post['login'])
                checking = check_password(post['password'], user.password)
                if checking:
                    login(request, user)
                    data = serializers.serialize("json", list(request.user.saves.all()))
                    des = json.loads(data)
                    new_des = list(map(change_load, des))
                    data = json.dumps(new_des)
                    return Response(data, status=status.HTTP_201_CREATED)
            return Response(json.dumps({
                'saves': 'error',
            }), status=status.HTTP_201_CREATED)
        except OperationalError:
            pass
    else:
        data = serializers.serialize("json", list(request.user.saves.all()))
        des = json.loads(data)
        new_des = list(map(change_load, des))
        data = json.dumps(new_des)
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def delete_save(request):
    data = request.data
    try:
        user = get_object_or_404(CustomAuth, username=data['user'])
    except OperationalError:
        pass
    time = data['time']
    time = ' '.join(time.split('T'))[0:-1]
    deler = None
    for i in user.saves.all():
        if time == str(i.save_date)[0:-9]:
            deler = i

    user.saves.remove(deler)
    with transaction.atomic():
        print(deler.country)
        deler.regions.all().delete()
        deler.country_ai.all().delete()
        deler.contracts.all().delete()
        deler.squad.all().delete()
        deler.squad_ai.all().delete()
        deler.relations.all().delete()

    deler.delete()

    data = serializers.serialize("json", list(user.saves.all()))
    des = json.loads(data)
    new_des = list(map(change_load, des))
    data = json.dumps(new_des)

    return Response(data, status=status.HTTP_201_CREATED)
