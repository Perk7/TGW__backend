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

def round_to_half(x):
    return round(x*2)/2

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

        obj = SaveContracts(con_type=reg.con_type, uniq=edited['country'], priority=reg.priority, deadline=reg.deadline)
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
                place = reg.place
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
                        place=reg.place
                    )
                    setSquad = SaveSquadAI.objects.all()
                    if setSquad:
                        obj.id = setSquad[len(setSquad)-1].id + 1
                    else:
                        obj.id = 1

                    obj.save()
                    edited['ai-squad'].append(obj)

    edited['buffs'] = CountryBonus(budget_infrastructure = round_to_half((edited['country'].export_trash +
                                                            edited['country'].get_pave_road() +
                                                            edited['country'].get_infrastructure() +
                                                            edited['country'].get_cargo_ship() +
                                                            edited['country'].get_people_ship())*2)/10,
                                   budget_education = round_to_half((edited['country'].education_quality +
                                                      edited['country'].education_avail)*5)/10,
                                   budget_research = round_to_half((edited['country'].alchemy +
                                                      edited['country'].magic +
                                                      edited['country'].technology +
                                                      edited['country'].science)*2.5)/10,
                                   budget_propaganda = round_to_half((2 - (edited['country'].support +
                                                       edited['country'].stability))*5)/10,
                                   budget_government = round_to_half((edited['country'].support +
                                                        edited['country'].stability)*5)/10)
    edited['buffs'].save()
    print(edited['buffs'])

    save_block = StartGame(
        country=edited['country'],
        buffs=edited['buffs']
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
@transaction.atomic
def save_game(request):
    data = request.data
    try:
        user = get_object_or_404(CustomAuth, username=data['auth'])
    except OperationalError:
        pass
    time = data['store']['save_date']
    time = ' '.join(time.split('T'))[0:-1]

    save = None
    for i in user.saves.all():
        if time == str(i.save_date)[0:-1]:
            save = i

    store = data['store']

# BUFFS
    save.buffs = CountryBonus(**store['buffs'])
    save.buffs.save()

# REGIONS
    for i in store['country']['regions']:
        reg = SaveRegions(**i)
        reg.save()
        save.regions.add(reg)
    for a in store['country_ai']:
        for i in a['regions']:
           reg = SaveRegions(**i)
           reg.save()
           save.regions.add(reg)

# COUNTRY
    capital = get_object_or_404(save.regions.all(), name=store['country']['capital']['name'])
    regs = []
    for i in store['country']['regions']:
        reg = get_object_or_404(save.regions.all(), name=i['name'])
        regs.append(reg)
    del store['country']['capital']
    del store['country']['regions']

    save.country = SaveCountry(**store['country'])
    save.country.capital = capital
    for i in regs:
        save.country.regions.add(i)
    save.country.save()

# COUNTRY_AI
    for coun in store['country_ai']:
        capital = get_object_or_404(save.regions.all(), name=coun['capital']['name'])
        regs = []
        for i in coun['regions']:
            reg = get_object_or_404(save.regions.all(), name=i['name'])
            regs.append(reg)
        del coun['capital']
        del coun['regions']

        cur_reg = get_object_or_404(save.country_ai.all(), identify=coun['identify'])
        cur_reg.delete()

        country = SaveCountryAI(**coun)
        country.capital = capital
        country.save()
        for i in regs:
            country.regions.add(i)
        country.save()
        save.country_ai.add(country)

# RELATIONS
    for i in store['relations']:
        coun = save.country
        pair = []
        for f in i['pair']:
            con = get_object_or_404(save.country_ai.all(), identify=f)
            pair.append(con)
        del i['pair']
        del i['uniq']

        reg = SaveRelations(**i)
        reg.uniq = coun
        reg.save()
        for f in pair:
            reg.pair.add(f)
        reg.save()

        save.relations.add(reg)

# CONTRACTS
    for i in store['contracts']:
        coun = save.country
        pair = []
        for f in i['pair']:
            con = get_object_or_404(save.country_ai.all(), identify=f)
            pair.append(con)
        del i['pair']
        del i['uniq']

        reg = SaveContracts(**i)
        reg.uniq = coun
        reg.save()
        for f in pair:
            reg.pair.add(f)
        reg.save()

        save.contracts.add(reg)

# SQUAD_AI
    for i in store['squad_ai']:
             coun = get_object_or_404(save.country_ai.all(), identify=i['country'])
             del i['country']
             reg = SaveSquadAI(**i)
             reg.save()
             reg.country = coun
             reg.save()
             save.squad_ai.add(reg)

# SQUAD
    for i in store['squad']:
             i['country'] = save.country
             reg = SaveSquad(**i)
             reg.save()
             save.squad.add(reg)

    save.save()

    user.saves.add(save)
    return Response(json.dumps(save.as_json()), status=status.HTTP_201_CREATED)
