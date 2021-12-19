from django.db.utils import OperationalError

from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from .models_main import Country, Regions, Squad
from .models_saves import SaveCountry, StartGame
from django.db import transaction

from django.contrib.auth import login
from .models_auth import CustomAuth
from django.contrib.auth.hashers import check_password

from typing import Literal, Union

def get_repr_government(type: Literal['O', 'M', 'D', 'R']) -> str:
    '''
    Return repr format of country government
    '''
    types = {
        'O': 'Ограниченная монархия',
        'M': 'Абсолютная монархия',
        'D':  'Однопартийная диктатура',
        'R': 'Республика',
    }

    return types[type]

def change_keys_to_values(country: dict) -> dict:
    """
    Serialize id and literals in country object to verbal
    """
    capital =  get_object_or_404(Regions, id=country['fields']['capital'])
    obj_country = get_object_or_404(Country, id=country['pk'])
    army = Squad.objects.filter(country = country['pk'])
    army_count = 0
    for i in army:
        army_count += i.summ()

    country['fields']['capital'] = capital.capital
    country['fields']['population'] = obj_country.get_population()
    country['fields']['gdp'] = obj_country.get_gdp()
    country['fields']['army'] = army_count
    regions = []

    for i in country['fields']['regions']:
        regions.append(get_object_or_404(Regions, id=i).name)
    country['fields']['regions'] = regions

    govern = country['fields']['government'][0]
    country['fields']['government'] = get_repr_government(govern)

    return country

def set_name_of_saved_game(save: dict) -> dict:
    """
    Set name of saved country on the high json level
    """
    saved_country = get_object_or_404(SaveCountry, id=save['fields']['country'])
    save['fields']['save_name'] = saved_country.name

    return save

def login_with_request_data(request: HttpRequest, req_data: dict) -> bool:
    """
    Try to login, if user not authorizied, and return status of auth
    """
    status = False
    try:
        if CustomAuth.objects.filter(username=req_data['login']):
            user = get_object_or_404(CustomAuth, username=req_data['login'])
            checking = check_password(req_data['password'], user.password)
            if checking:
                status = True
                login(request, user)
    except OperationalError:
        status = False

    return status

def get_save_by_save_time(user: CustomAuth, req_data: dict) -> Union[StartGame, bool]:
    """
    
    """
    save_time = req_data['time']
    save_time = ' '.join(save_time.split('T'))[0:-1]
    save = None
    for i in user.saves.all():
        if save_time == str(i.save_date)[0:-9]:
            save = i

    return save if save else False

def delete_save_by_object(user: CustomAuth, save: StartGame) -> CustomAuth:
    """
    Delete save by orm of this save
    """
    user.saves.remove(save)
    with transaction.atomic():
        save.regions.all().delete()
        save.country_ai.all().delete()
        save.contracts.all().delete()
        save.squad.all().delete()
        save.squad_ai.all().delete()
        save.relations.all().delete()
        save.buffs.delete()

    save.delete()

    return user