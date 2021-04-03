from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import os
import openpyxl

from .models_main import Country, Regions, Squad, Relations, Tax, Contracts

def index(request):
	return render(request, 'index.html')

def excel(request):
    base_dir = settings.MEDIA_ROOT
    path = os.path.join(base_dir, "excel.xlsx")
    my_wb_obj = openpyxl.load_workbook(path)
    sheet_ranges = my_wb_obj.active

    for model in (Regions, Squad, Country, Relations, Tax, Contracts):
        items = model.objects.all()
        items.delete()

    # Regions
    for x in sheet_ranges['C':'BZ']:
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

                        industry_blackmetall = x[20].value,
                        industry_colormetall = x[21].value,
                        industry_coal = x[22].value,

                        industry_hunting = x[23].value,
                        industry_fishing = x[24].value,

                        industry_forestry = x[25].value,

                        industry_blacksmith = x[26].value,

                        industry_animals = x[27].value,
                        industry_vegetable = x[28].value,
                        industry_wheat = x[29].value,
                        industry_typography = x[30].value,

                        industry_light = x[31].value,

                        industry_eating = x[32].value,

                        industry_jewelry = x[33].value,

                        industry_transport = x[34].value,

                        industry_alchemy = x[35].value,

                        industry_hiring = x[36].value,

                        industry_culture = x[37].value,

                        industry_other = x[38].value,
                        )
        obj.save()

    items = Country.objects.all()
    items.delete()
    regs = Regions.objects.all()
    i = 0

    # Tax
    for x in sheet_ranges['B':'AE']:
        obj = Tax(
            tax_type=x[144].value,
            name=x[145].value,
            status=x[146].value,
            value=float(x[147].value)
        )

        obj.save()

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
                        )
        obj.save()

        if x[111].value:
            regions = x[111].value.split(',')
            for reg in regions:
                side = get_object_or_404(Regions, name=reg)
                obj.regions.add(side.id)

        for i in range(112, 118):
            pair_one = get_object_or_404(Tax, name=sheet_ranges['A'][i].value, value=x[i].value)
            obj.taxes.add(pair_one.id)

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
    for x in sheet_ranges['B':'CE']:
        country = get_object_or_404(Country, name=x[169].value)

        obj = Squad(
            pechot_quan = x[159].value,
            archer_quan = x[160].value,
            cavallery_quan = x[161].value,

            catapult_quan = x[163].value,

            esmin_quan = x[165].value,
            linkor_quan = x[166].value,

            place_type = str(x[168].value).upper(),

            country = country,

            status = str(x[170].value).upper()
        )

        obj.save()

    # Contracts
    for x in sheet_ranges['B':'EI']:
        obj = Contracts(
            con_type = x[154].value,
        )

        obj.save()

        pair_one = get_object_or_404(Country, name=x[152].value)
        obj.pair.add(pair_one.id)
        pair_one = get_object_or_404(Country, name=x[153].value)
        obj.pair.add(pair_one.id)

    return redirect('/admin')