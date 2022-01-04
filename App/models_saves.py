from django.db import models
import datetime 
from django.utils.timezone import get_current_timezone, now
from App.models_abstract import Abstract_Regions, Abstract_Country, Abstract_Contracts, Abstract_Relations, Abstract_Squad

class SaveRegions(Abstract_Regions):

	def get_gdp(self):
		attr = [a for a in dir(SaveRegions) if a.startswith('industry')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def get_needs(self):
		attr = [a for a in dir(SaveRegions) if a.startswith('needs')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Save Регион'
		verbose_name_plural = 'Save Регионы'

	def as_json(self):
		a = self.__dict__
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b

class SaveCountry(Abstract_Country):
	regions = models.ManyToManyField(SaveRegions)
	capital = models.OneToOneField(SaveRegions, on_delete=models.CASCADE, related_name='region_capital')

	def get_gdp(self):
		attr = [func for func in dir(SaveCountry) if
				callable(getattr(SaveCountry, func)) and func.startswith('get_industry')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)()
		return summ

	def get_needs(self):
		attr = [a() for a in dir(SaveCountry) if a.startswith('get_needs')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Save Страна'
		verbose_name_plural = 'Save Страны'

	def as_json(self):
		a = self.__dict__
		a['regions'] = [SaveRegions.objects.filter(id=i.id)[0].as_json() for i in list(self.regions.all())]
		a['capital'] = self.capital.as_json()
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b

class SaveCountryAI(models.Model):
	name = models.CharField(max_length=30, default='Default country')
	regions = models.ManyToManyField(SaveRegions)
	capital = models.OneToOneField(SaveRegions, on_delete=models.CASCADE, related_name='AI_region_capital')
	identify = models.CharField(max_length=50, default='empire', blank=True)

	def get_population(self):
		summ = 0
		for i in self.regions.all():
			summ += i.population
		return summ

	def get_area(self):
		summ = 0
		for i in self.regions.all():
			summ += i.area
		return summ

	def get_avg_salary(self):
		summ = 0
		for i in self.regions.all():
			summ += i.avg_salary
		return summ / len(self.regions.all())

	def get_infrastructure(self):
		summ = 0
		for i in self.regions.all():
			summ += i.infrastructure
		return summ / len(self.regions.all())

	education_quality = models.FloatField(default=0.6)

	support = models.FloatField(default=0.6)
	stability = models.FloatField(default=0.6)

	government = models.CharField(max_length=7, default='m,t,a,p')
	area_format = models.CharField(max_length=7, default='c,p,l,e')

	army_quality = models.FloatField(default=0.5)

	tax_physic = models.CharField(max_length=7, default='d,z')
	tax_jurid = models.CharField(max_length=7, default='p,i,g,e')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Save ИИ_Страна'
		verbose_name_plural = 'Save ИИ_Страны'

	def as_json(self):
		return dict(
    		name=self.name,
    		regions=[SaveRegions.objects.filter(id=i.id)[0].as_json() for i in list(self.regions.all())],
    		capital=self.capital.as_json(),
    		identify = self.identify,
    		education_quality = self.education_quality,
    		support = self.support,
    		stability = self.stability,
    		government = self.government,
    		area_format = self.area_format,
    		army_quality = self.army_quality,
    		tax_physic = self.tax_physic,
            tax_jurid = self.tax_jurid
    	)

class SaveRelations(Abstract_Relations):

	pair = models.ManyToManyField(SaveCountryAI)
	uniq = models.ForeignKey(SaveCountry, on_delete=models.CASCADE)

	def __str__(self):
		if len(self.pair.all()) == 2:
			return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + str(self.value)
		elif len(self.pair.all()) == 1:
			return self.pair.all()[0].name + '-' + self.uniq.name + ' : ' + str(self.value)
		else:
			return 'none relations'

	class Meta:
		verbose_name = 'Save Отношение'
		verbose_name_plural = 'Save Отношения'

	def as_json(self):
		a = self.__dict__
		a['pair'] = [i.identify for i in list(self.pair.all())]
		a['uniq'] = self.uniq.identify
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b


class SaveContracts(Abstract_Contracts):

	pair = models.ManyToManyField(SaveCountryAI)
	uniq = models.ForeignKey(SaveCountry, on_delete=models.CASCADE)

	def __str__(self):
		if len(self.pair.all()) == 2:
			return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + str(self.con_type)
		else:
			return self.pair.all()[0].name + '-' + self.uniq.name + ' : ' + str(self.con_type)

	class Meta:
		verbose_name = 'Save Договор'
		verbose_name_plural = 'Save Договора'

	def as_json(self):
		a = self.__dict__
		a['pair'] = [i.identify for i in list(self.pair.all())]
		a['uniq'] = self.uniq.identify
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b

class SaveSquadAI(Abstract_Squad):

	country = models.ForeignKey(SaveCountryAI, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.country.name + ' : ' + str(self.summ()) + ' ' + str(self.id)

	class Meta:
		verbose_name = 'Save ИИ_Отряд'
		verbose_name_plural = 'Save ИИ_Отряды'

	def as_json(self):
		a = self.__dict__
		a['country'] = self.country.identify
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b

class SaveSquad(Abstract_Squad):

	country = models.ForeignKey(SaveCountry, on_delete=models.CASCADE)

	def __str__(self):
		return self.country.name + ' : ' + str(self.summ())

	class Meta:
		verbose_name = 'Save Отряд'
		verbose_name_plural = 'Save Отряды'

	def as_json(self):
		a = self.__dict__
		a['country'] = self.country.identify
		b = {}
		for i in a:
			if i != '_state':
				b[i] = a[i]
		return b

class CountryBonus(models.Model):
    step = models.IntegerField(default=1)
    actions = models.IntegerField(default=10)

    support = models.FloatField(default=0)
    stability = models.FloatField(default=0)

    population = models.FloatField(default=0)

    inflation = models.FloatField(default=0)
    poverty = models.FloatField(default=0)
    unemployment = models.FloatField(default=0)
    avg_salary = models.FloatField(default=0)

    infrastructure = models.FloatField(default=0)
    stone_road = models.FloatField(default=0)
    trash = models.FloatField(default=0)
    port = models.FloatField(default=0)
    delivery_box = models.FloatField(default=0)
    delivery_people = models.FloatField(default=0)

    alchemy = models.FloatField(default=0)
    magic = models.FloatField(default=0)
    science = models.FloatField(default=0)
    technology = models.FloatField(default=0)

    education_quality = models.FloatField(default=0)
    education_access = models.FloatField(default=0)

    army_quality = models.FloatField(default=0.4)

    industry_blackmetall = models.FloatField(default=0)
    industry_colormetall = models.FloatField(default=0)
    industry_coal = models.FloatField(default=0)
    industry_hunting = models.FloatField(default=0)
    industry_fishing = models.FloatField(default=0)
    industry_forestry = models.FloatField(default=0)
    industry_blacksmith = models.FloatField(default=0)
    industry_animals = models.FloatField(default=0)
    industry_vegetable = models.FloatField(default=0)
    industry_wheat = models.FloatField(default=0)
    industry_typography = models.FloatField(default=0)
    industry_light = models.FloatField(default=0)
    industry_eating = models.FloatField(default=0)
    industry_jewelry = models.FloatField(default=0)
    industry_transport = models.FloatField(default=0)
    industry_alchemy = models.FloatField(default=0)
    industry_hiring = models.FloatField(default=0)
    industry_culture = models.FloatField(default=0)
    industry_other = models.FloatField(default=0)

    budget_infrastructure = models.FloatField(default=0.5)
    budget_education = models.FloatField(default=0.5)
    budget_research = models.FloatField(default=0.5)
    budget_propaganda = models.FloatField(default=0.5)
    budget_government = models.FloatField(default=0.5)

    kazna = models.IntegerField(default=10_000_000)

    class Meta:
        verbose_name = 'Save Баффы'
        verbose_name_plural = 'Save Баффы'

    def as_json(self):
        a = self.__dict__
        b = {}
        for i in a:
            if i != '_state':
                b[i] = a[i]	
        return b

def getTime():
	return datetime.datetime.utcnow().replace(tzinfo=get_current_timezone())

class StartGame(models.Model):
	save_date = models.DateTimeField(default=datetime.datetime.now)

	buffs = models.OneToOneField(CountryBonus, on_delete=models.CASCADE)

	country = models.OneToOneField(SaveCountry, on_delete=models.CASCADE)
	regions = models.ManyToManyField(SaveRegions)
	relations = models.ManyToManyField(SaveRelations)
	contracts = models.ManyToManyField(SaveContracts)
	squad_ai = models.ManyToManyField(SaveSquadAI)
	squad = models.ManyToManyField(SaveSquad)
	country_ai = models.ManyToManyField(SaveCountryAI)

	def __str__(self):
		return str(self.country) + ' ' + str(self.save_date)

	class Meta:
		verbose_name = 'Save'
		verbose_name_plural = 'Saves'

	def as_json(self):
		return dict(
			save_date = str(self.save_date),
			country = self.country.as_json(),
            buffs = self.buffs.as_json(),
			relations = [SaveRelations.objects.filter(id=i.id)[0].as_json() for i in list(self.relations.all())],
			contracts = [SaveContracts.objects.filter(id=i.id)[0].as_json() for i in list(self.contracts.all())],
			squad_ai = [SaveSquadAI.objects.filter(id=i.id)[0].as_json() for i in list(self.squad_ai.all())],
			squad = [SaveSquad.objects.filter(id=i.id)[0].as_json() for i in list(self.squad.all())],
			country_ai = [SaveCountryAI.objects.filter(id=i.id)[0].as_json() for i in list(self.country_ai.all())],
		)