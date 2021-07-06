from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

from django.db import transaction
import random
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view
import json
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models_auth import CustomAuth
from django.core import serializers

from django.db.utils import OperationalError

from .models_saves import *
from .models_main import *


@api_view(['POST'])
@transaction.atomic
def start_game(request):
    req_country = request.data['country']
    req_user = request.data['user']
    country = get_object_or_404(Country, identify=req_country)
    try:
        user = get_object_or_404(CustomAuth, username=req_user)
    except OperationalError:
        pass

    saves = {
        'regions' : [],
        'ai-country' : [],
        'country' : [],
        'contracts' : [],
        'squads' : [],
        'relations' : [],
             }

    for reg in Regions.objects.all():
        saves['regions'].append(reg)

    for coun in Country.objects.exclude(identify=req_country):
        saves['ai-country'].append(coun)

    saves['country'].append(country)

    for contr in Contracts.objects.all():
        saves['contracts'].append(contr)

    for relat in Relations.objects.all():
        saves['relations'].append(relat)

    for squad in Squad.objects.all():
        saves['squads'].append(squad)

    edited = {
        'regions' : [],
        'ai-country' : [],
        'relations' : [],
        'contracts' : [],
        'squad' : [],
        'ai-squad' : [],
            }

    for reg in saves['regions']:
        reg_dict = reg.__dict__
        del reg_dict['_state']
        del reg_dict['id']

        obj = SaveRegions(**reg_dict)
        obj.save()
        edited['regions'].append(obj)

    for con in saves['ai-country']:
        regs = con.regions.all()

        capital = None
        for i in edited['regions']:
            if con.capital.name == i.name:
                capital = i

        ai = SaveCountryAI(
            name = con.name,
            capital = capital,
            identify = con.identify,
            education_quality = con.education_quality,
            support = con.support,
            stability = con.stability,
            government = con.government,
            area_format = con.area_format

        )
        ai.save()

        for i in regs:
            reg = None
            for r in edited['regions']:
                if i.name == r.name:
                    reg = r
            ai.regions.add(reg.id)

        edited['ai-country'].append(ai)

    for coun in saves['country']:
        coun_dict = coun.__dict__
        del coun_dict['_state']
        del coun_dict['id']

        a = get_object_or_404(Country, name=coun.name)
        regs = a.regions.all()

        capital = None
        for i in edited['regions']:
            if a.capital.name == i.name:
                capital = i
        coun_dict['capital_id'] = capital.id

        obj = SaveCountry(**coun_dict)
        obj.save()

        for i in regs:
            reg = None
            for r in edited['regions']:
                if i.name == r.name:
                    reg = r
            obj.regions.add(reg.id)

        edited['country'] = obj

    for reg in saves['relations']:
        f = reg.pair.all()

        obj = SaveRelations(value=reg.value, uniq=edited['country'])
        obj.save()

        for i in f:
            if i.name == edited['country'].name:
                obj.uniq = SaveCountry.objects.get(id=edited['country'].id)
            for d in edited['ai-country']:
                if i.name == d.name:
                    obj.pair.add(d.id)
        edited['relations'].append(obj)

    for reg in saves['contracts']:
        f = reg.pair.all()

        obj = SaveContracts(con_type=reg.con_type, uniq=edited['country'], priority=reg.priority)
        obj.save()

        for i in f:
            if i.name == edited['country'].name:
                obj.uniq = SaveCountry.objects.get(id=edited['country'].id)
            for d in edited['ai-country']:
                if i.name == d.name:
                    obj.pair.add(d.id)
        edited['contracts'].append(obj)

    for reg in saves['squads']:
        if reg.country.name == edited['country'].name:
            obj = SaveSquad(
                country = edited['country'],
                pechot_quan = reg.pechot_quan,
                archer_quan = reg.archer_quan,
                cavallery_quan = reg.cavallery_quan,
                catapult_quan = reg.catapult_quan,
                place_type = reg.place_type,
                status = reg.status,
            )
            obj.save()
            edited['squad'].append(obj)
        else:
            for i in edited['ai-country']:
                if reg.country.name == i.name:
                    coun = i
                    obj = SaveSquadAI(
                        country=coun,
                        pechot_quan=reg.pechot_quan,
                        archer_quan=reg.archer_quan,
                        cavallery_quan=reg.cavallery_quan,
                        catapult_quan=reg.catapult_quan,
                        place_type=reg.place_type,
                        status=reg.status,
                    )
                    setSquad = SaveSquadAI.objects.all()
                    if setSquad:
                        obj.id = setSquad[len(setSquad)-1].id + 1
                    else:
                        obj.id = 1

                    obj.save()
                    edited['ai-squad'].append(obj)

    save_block = StartGame(
        country=edited['country']
    )
    save_block.save()
    for i in edited['regions']:
        save_block.regions.add(i.id)
    for i in edited['relations']:
        save_block.relations.add(i.id)
    for i in edited['contracts']:
        save_block.contracts.add(i.id)
    for i in edited['ai-squad']:
        if i.country:
            save_block.squad_ai.add(i.id)
    for i in edited['squad']:
        save_block.squad.add(i.id)
    for i in edited['ai-country']:
        save_block.country_ai.add(i.id)

    user.saves.add(save_block)

    user.active_save = save_block.id
    user.save()

    data = json.dumps(save_block.as_json())

    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def load_game(request):
    data = request.data
    try:
        user = get_object_or_404(CustomAuth, username=data['user'])
    except OperationalError:
        pass
    time = data['time']
    time = ' '.join(time.split('T'))[0:-1]

    save = None
    for i in user.saves.all():
        if time == str(i.save_date)[0:-9]:
            save = i

    user.active_save = save.id
    user.save()

    data = json.dumps(save.as_json())

    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def get_active_game(request):
    print(request.data)
    data = request.data
    try:
        user = get_object_or_404(CustomAuth, username=data['user'])
    except OperationalError:
        pass
    save = get_object_or_404(StartGame, id=user.active_save)

    data = json.dumps(save.as_json())

    return Response(data, status=status.HTTP_201_CREATED)