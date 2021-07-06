from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import os
import openpyxl

from .models_main import Country, Regions, Squad, Relations, Contracts

from .models_saves import *

def index(request):
	return render(request, 'index.html')

def clear(request):
    SaveSquad.objects.all().delete()
    SaveSquadAI.objects.all().delete()
    SaveContracts.objects.all().delete()
    SaveCountry.objects.all().delete()
    SaveRelations.objects.all().delete()
    SaveRegions.objects.all().delete()
    SaveCountryAI.objects.all().delete()

    StartGame.objects.all().delete()

def excel(request):
    base_dir = settings.MEDIA_ROOT
    path = os.path.join(base_dir, "excel.xlsx")
    my_wb_obj = openpyxl.load_workbook(path)
    sheet_ranges = my_wb_obj.active

    for model in (Regions, Squad, Country, Relations, Contracts):
        items = model.objects.all()
        if items:
            items.delete()

    # Regions
    for x in sheet_ranges['C':'CA']:
        print()
        obj = Regions(
                        name = x[0].value,
                        capital = x[1].value,
                        population = x[2].value,
                        area = x[3].value,
                        universities = x[4].value,
                        schools = x[5].value,
                        aqueducs = x[6].value,
                        stone_road = x[7].value,
                        pave_road = x[8].value,
                        poverty = x[9].value,
                        unemployment = x[10].value,
                        avg_salary = x[11].value,
                        seaside = bool(x[12].value),
                        infrastructure = x[13].value,
                        port = x[14].value if x[14].value else 0,
                        cargo_ship = x[15].value,
                        people_ship =x[16].value,

                        industry_blackmetall = x[20].value*1000,
                        industry_colormetall = x[21].value*1000,
                        industry_coal = x[22].value*1000,

                        industry_hunting = x[23].value*1000,
                        industry_fishing = x[24].value*1000,

                        industry_forestry = x[25].value*1000,

                        industry_blacksmith = x[26].value*1000,

                        industry_animals = x[27].value*1000,
                        industry_vegetable = x[28].value*1000,
                        industry_wheat = x[29].value*1000,
                        industry_typography = x[30].value*1000,

                        industry_light = x[31].value*1000,

                        industry_eating = x[32].value*1000,

                        industry_jewelry = x[33].value*1000,

                        industry_transport = x[34].value*1000,

                        industry_alchemy = x[35].value*1000,

                        industry_hiring = x[36].value*1000,

                        industry_culture = x[37].value*1000,

                        industry_other = x[38].value*1000,

                        needs_blackmetall = x[41].value*1000,

                        needs_colormetall = x[42].value*1000,
                        needs_coal = x[43].value*1000,

                        needs_hunting = x[44].value*1000,
                        needs_fishing = x[45].value*1000,

                        needs_forestry = x[46].value*1000,

                        needs_blacksmith = x[47].value*1000,

                        needs_animals = x[48].value*1000,
                        needs_vegetable = x[49].value*1000,
                        needs_wheat = x[50].value*1000,
                        needs_typography = x[51].value*1000,

                        needs_light = x[52].value*1000,

                        needs_eating = x[53].value*1000,

                        needs_jewelry = x[54].value*1000,

                        needs_transport = x[55].value*1000,

                        needs_alchemy = x[56].value*1000,

                        needs_hiring = x[57].value*1000,

                        needs_culture = x[58].value*1000,

                        needs_other = x[59].value*1000,
                                                )
        obj.save()

    items = Country.objects.all()
    items.delete()
    regs = Regions.objects.all()
    i = 0

    # Countries
    for x in sheet_ranges['C':'W']:
        i += 1
        print()
        obj = Country(
                        name = x[67].value,
                        capital = get_object_or_404(Regions, capital=x[66].value),
                        identify = x[68].value,
                        education_quality = x[69].value,
                        education_avail = x[70].value,
                        alchemy = x[71].value,
                        magic = x[72].value,
                        science = x[73].value,
                        technology = x[74].value,
                        export_trash = x[75].value,

                        support = x[77].value,
                        stability = x[78].value,
                        government = x[79].value,
                        area_format = x[80].value,

                        maternal_capital = x[82].value,
                        allowance_unemploy = x[83].value,
                        allowance_disability = x[84].value,
                        pension_m = x[85].value,
                        pension_w = x[86].value,
                        avg_pension = x[87].value,

                        army_salary = x[89].value,
                        army_maintain = x[90].value,
                        army_equip = x[91].value,

                        inflation = x[93].value,

                        law_equal_rights = bool(x[95].value),
                        law_torture = bool(x[96].value),
                        law_speech = bool(x[97].value),
                        law_demonstration = bool(x[98].value),
                        law_property = bool(x[99].value),
                        law_creation = bool(x[100].value),
                        law_rasism = bool(x[101].value),
                        law_heritage = bool(x[102].value),
                        law_slavery = bool(x[103].value),
                        law_court = bool(x[104].value),
                        law_child_labour = bool(x[105].value),
                        law_monopoly = bool(x[106].value),
                        law_free_enterspire = bool(x[107].value),
                        law_work_day_limit = bool(x[108].value),
                        law_death_penalty = bool(x[109].value),

                        tax_physic=x[144].value,
                        tax_jurid=x[145].value,
                        )
        obj.save()

        if x[111].value:
            regions = x[111].value.split(',')
            for reg in regions:
                side = get_object_or_404(Regions, name=reg)
                obj.regions.add(side.id)

    # Relations
    start = 120
    column = sheet_ranges['A']
    for x in sheet_ranges['B':'U']:
        for i in range(start, 140):
            obj = Relations(value = x[i].value)
            obj.save()
            pair_one = get_object_or_404(Country, name=x[118].value)
            obj.pair.add(pair_one.id)
            pair_one = get_object_or_404(Country, name=column[i].value)
            obj.pair.add(pair_one.id)

        start += 1

    # Squad
    for x in sheet_ranges['B':'BL']:
        country = get_object_or_404(Country, name=x[169].value)

        obj = Squad(
            pechot_quan = x[159].value,
            archer_quan = x[160].value,
            cavallery_quan = x[161].value,

            catapult_quan = x[163].value,

            place_type = str(x[168].value).upper(),

            country = country,

            status = str(x[170].value).upper()
        )

        obj.save()

    # Contracts
    for x in sheet_ranges['B':'EJ']:
        obj = Contracts(
            con_type = x[154].value,
            priority = x[155].value,
        )

        obj.save()

        pair_one = get_object_or_404(Country, name=x[152].value)
        obj.pair.add(pair_one.id)
        pair_one = get_object_or_404(Country, name=x[153].value)
        obj.pair.add(pair_one.id)

    return redirect('/admin')