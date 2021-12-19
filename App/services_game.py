from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404
from Game.TGW.App.models_auth import CustomAuth
from typing import Union

from .models_saves import *
from .models_main import *

def round_to_half(x):
    return round(x*2)/2

def create_new_game(user: str, country: str) -> Union(StartGame | dict):
    """
    Creaitng new StartGame object model for user with needed country
    """
    try:
        country = get_object_or_404(Country, identify=country)
        user = get_object_or_404(CustomAuth, username=user)
    except OperationalError:
        return {}

    saves = {
        'regions' : [],
        'ai-country' : [],
        'country' : [],
        'contracts' : [],
        'squads' : [],
        'relations' : [],
    }

    for coun in Country.objects.exclude(identify=country):
        saves['ai-country'].append(coun)

    saves['country'].append(country)

    for i in [ [Regions, 'regions'], [Contracts, 'contracts'], [Relations, 'relations'], [Squad, 'squad'] ]:
        for obj in i[0].objects.all():
            saves[i[1]].append(obj)

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

    save_block = StartGame(
        country=edited['country'],
        buffs=edited['buffs']
    )
    save_block.save()

    for i in [ 'regions', 'relations', 'squad', 'contracts' ]:
        for i in edited[i]:
            save_block.__getattribute__(i).add(i.id)

    for i in edited['ai-country']:
        save_block.country_ai.add(i.id)

    for i in edited['ai-squad']:
        if i.country:
            save_block.squad_ai.add(i.id)

    user.saves.add(save_block)

    user.active_save = save_block.id
    user.save()

    return save_block

def find_saved_game_by_time(user: CustomAuth, time: str) -> StartGame:
    """
    Parsing time format and find needing StartGame object
    """
    time = ' '.join(time.split('T'))[0:-1]

    save = None
    for i in user.saves.all():
        if time == str(i.save_date)[0:-9]:
            save = i
    
    return save

def load_game_by_time(user: str, time: str) -> StartGame:
    """
    Find having StartGame object of user by time
    """
    try:
        user = get_object_or_404(CustomAuth, username=user)
    except OperationalError:
        return {}

    save = find_saved_game_by_time(user, time)

    user.active_save = save.id
    user.save()

    return save

def save_current_game(user: str, store: dict) -> Union(dict | StartGame):
    """
    Saving game (Update having fields object)
    """
    try:
        user = get_object_or_404(CustomAuth, username=user)
    except OperationalError:
        return {}

    time = store['save_date']
    save = find_saved_game_by_time(user, time)

    # Buffs
    save.buffs = CountryBonus(**store['buffs'])
    save.buffs.save()

    # Regions
    for i in store['country']['regions']:
        reg = SaveRegions(**i)
        reg.save()
        save.regions.add(reg)
    for a in store['country_ai']:
        for i in a['regions']:
           reg = SaveRegions(**i)
           reg.save()
           save.regions.add(reg)

    # Country
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

    # Country_ai
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

    # Relations
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

    # Contracts
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

    # Squad_ai
    for i in store['squad_ai']:
             coun = get_object_or_404(save.country_ai.all(), identify=i['country'])
             del i['country']
             reg = SaveSquadAI(**i)
             reg.save()
             reg.country = coun
             reg.save()
             save.squad_ai.add(reg)

    # Squad
    for i in store['squad']:
             i['country'] = save.country
             reg = SaveSquad(**i)
             reg.save()
             save.squad.add(reg)

    save.save()

    user.saves.add(save)

    return save