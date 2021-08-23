from django.contrib import admin
from .models_main import Country, Relations, Regions, Contracts, Squad
from .models_auth import CustomAuth
from .models_saves import StartGame, SaveRegions, SaveCountry, SaveRelations, SaveContracts, SaveSquad, SaveCountryAI, SaveSquadAI, CountryBonus

admin.site.register(CustomAuth)

admin.site.register(Regions)
admin.site.register(Country)
admin.site.register(Relations)
admin.site.register(Contracts)
admin.site.register(Squad)

admin.site.register(StartGame)
admin.site.register(SaveRegions)
admin.site.register(SaveCountry)
admin.site.register(SaveRelations)
admin.site.register(SaveContracts)
admin.site.register(SaveSquad)
admin.site.register(SaveSquadAI)
admin.site.register(SaveCountryAI)

admin.site.register(CountryBonus)