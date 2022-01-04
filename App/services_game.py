from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404
from .models_auth import CustomAuth
from typing import Dict, List, Literal, Union

from .models_saves import *
from .models_main import *

def round_to_half(x):
    return round(x*2)/2

def make_save_regions(regions: List[Regions]) -> List[SaveRegions]:
    """
    Copy Regions to SaveRegions and return arr of its regions
    """
    edited = []
    for reg in regions:
        reg_dict = reg.__dict__
        del reg_dict['_state']
        del reg_dict['id']

        obj = SaveRegions(**reg_dict)
        obj.save()
        edited.append(obj)

    return edited

def make_save_ai_countries(countries: List[Country], regions: List[SaveRegions]) -> List[SaveCountryAI]:
    """
    Copy Countries to SaveCountryAI and return arr of its countries
    """
    edited = []
    for con in countries:
        regs = con.regions.all()

        capital = None
        for i in regions:
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
            for r in regions:
                if i.name == r.name:
                    reg = r
            ai.regions.add(reg.id)

        edited.append(ai)

    return edited

def make_save_country(country: Country, regions: List[SaveRegions]) -> SaveCountry:
    """
    Copy Country to SaveCountry and return arr of it object
    """
    coun_dict = country.__dict__
    del coun_dict['_state']
    del coun_dict['id']

    a = get_object_or_404(Country, name=country.name)
    regs = a.regions.all()

    capital = None
    for i in regions:
        if a.capital.name == i.name:
            capital = i
    coun_dict['capital_id'] = capital.id

    obj = SaveCountry(**coun_dict)
    obj.save()

    for i in regs:
        reg = None
        for r in regions:
            if i.name == r.name:
                reg = r
        obj.regions.add(reg.id)

    return obj

def make_save_relations(relations: List[Relations], country: SaveCountry, ai_countries: List[SaveCountryAI]) -> List[SaveRelations]:
    """
    Copy Relations to SaveRelations and return arr of its countries
    """
    edited = []
    for reg in relations:
        f = reg.pair.all()

        obj = SaveRelations(value=reg.value, uniq=country)
        obj.save()

        for i in f:
            if i.name == country.name:
                obj.uniq = SaveCountry.objects.get(id=country.id)
            for d in ai_countries:
                if i.name == d.name:
                    obj.pair.add(d.id)
        edited.append(obj)

    return edited

def make_save_contracts(contracts: List[Contracts], country: SaveCountry, ai_countries: List[SaveCountryAI]) -> List[SaveContracts]:
    """
    Copy Contracts to SaveContracts and return arr of its countries
    """
    edited = []
    for reg in contracts:
        f = reg.pair.all()

        obj = SaveContracts(con_type=reg.con_type, uniq=country, priority=reg.priority, deadline=reg.deadline)
        obj.save()

        for i in f:
            if i.name == country.name:
                obj.uniq = SaveCountry.objects.get(id=country.id)
            for d in ai_countries:
                if i.name == d.name:
                    obj.pair.add(d.id)
        edited.append(obj)

    return edited

type_squads_name = Literal['ai', 'own']
type_squads_arr = Union[List[SaveSquad], List[SaveSquadAI]]
def make_save_squads(squads: List[Squad], country: SaveCountry, ai_countries: List[SaveCountryAI]) -> Dict[type_squads_name, type_squads_arr]:
    """
    Copy Squads to SaveSquads and SaveSquadsAI and return dict of own and ai objects
    """
    own_squads = []
    ai_squads = []

    for reg in squads:
        if reg.country.name == country.name:
            obj = SaveSquad(
                country = country,
                pechot_quan = reg.pechot_quan,
                archer_quan = reg.archer_quan,
                cavallery_quan = reg.cavallery_quan,
                catapult_quan = reg.catapult_quan,
                place_type = reg.place_type,
                status = reg.status,
                place = reg.place
            )
            obj.save()
            own_squads.append(obj)
        else:
            for i in ai_countries:
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
                    ai_squads.append(obj)
    
    return {
        'own': own_squads,
        'ai': ai_squads
    }

def create_new_game(user: str, country: str) -> Union[StartGame, dict]:
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
        'ai-country' : [coun for coun in Country.objects.exclude(identify=country)],
        'country' : country,
        'contracts' : [],
        'squads' : [],
        'relations' : [],
    }

    for i in [ [Regions, 'regions'], [Contracts, 'contracts'], [Relations, 'relations'], [Squad, 'squads'] ]:
        for obj in i[0].objects.all():
            saves[i[1]].append(obj)

    edited = {
        'regions' : make_save_regions(saves['regions']),
        'ai-country' : [],
        'relations' : [],
        'contracts' : [],
        'squad' : [],
        'ai-squad' : [],
    }

    edited['ai-country'] = make_save_ai_countries(saves['ai-country'], edited['regions'])
    edited['country'] = make_save_country(saves['country'], edited['regions'])  
    edited['relations'] = make_save_relations(saves['relations'], edited['country'], edited['ai-country'])
    edited['contracts'] = make_save_contracts(saves['contracts'], edited['country'], edited['ai-country'])
    
    squads = make_save_squads(saves['squads'], edited['country'], edited['ai-country'])
    edited['squad'], edited['ai-squad'] = squads['own'], squads['ai']

    edited['buffs'] = CountryBonus(budget_infrastructure = round_to_half((edited['country'].export_trash +
                                                            edited['country'].get_stone_road() +
                                                            edited['country'].get_infrastructure() +
                                                            edited['country'].get_cargo_ship() +
                                                            edited['country'].get_people_ship())*2)/10,
                                   budget_education = round_to_half((edited['country'].education_quality +
                                                      edited['country'].education_quality)*5)/10,
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
        for x in edited[i]:
            save_block.__getattribute__(i).add(x.id)

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
    time = ' '.join(time.split('T'))[0:-7]

    save = None
    for i in user.saves.all():
        if time == str(i.save_date)[0:-7]:
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

def save_current_game(user: str, store: dict) -> Union[dict, StartGame]:
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
    for a in store['country_ai'] + [store['country']]:
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

    # Relations and contracts
    cur_arr = store['relations'] + store['contracts']
    for i in range(len(cur_arr)):
        coun = save.country
        pair = []
        for f in cur_arr[i]['pair']:
            con = get_object_or_404(save.country_ai.all(), identify=f)
            pair.append(con)
        del cur_arr[i]['pair']
        del cur_arr[i]['uniq']

        class_type = [SaveRelations, 'relations'] if i < len(store['relations']) else [SaveContracts, 'contracts']

        reg = class_type[0](**cur_arr[i])
        reg.uniq = coun
        reg.save()
        for f in pair:
            reg.pair.add(f)
        reg.save()

        save.__getattribute__(class_type[1]).add(reg)

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