from django.db import models

class Regions(models.Model):		
	
	# Main properties
	name = models.CharField(max_length=20, default='Default region', unique=True)
	capital = models.CharField(max_length=20, default='Default city', unique=True)
	population = models.IntegerField(default=500_000)
	area = models.IntegerField(default=100)
	universities = models.IntegerField(default=5)
	schools = models.IntegerField(default=15)
	aqueducs = models.IntegerField(default=30)
	stone_road = models.FloatField(default=0.4)
	pave_road = models.FloatField(default=0.1)
	poverty = models.FloatField(default=0.2)
	unemployment = models.FloatField(default=0.08)
	avg_salary = models.IntegerField(default=2500)
	seaside = models.BooleanField(default=False)
	infrastructure = models.FloatField(default=0.5)
	port = models.FloatField(default=0.6, blank=True)
	cargo_ship = models.FloatField(default=0.6)
	people_ship = models.FloatField(default=0.6)
	
	# Industries of economy
	industry_blackmetall = models.IntegerField(default=700_000_000)
	industry_colormetall = models.IntegerField(default=400_000_000)
	industry_coal = models.IntegerField(default=200_000_000)

	industry_hunting = models.IntegerField(default=300_000_000)
	industry_fishing = models.IntegerField(default=300_000_000)

	industry_forestry = models.IntegerField(default=500_000_000)

	industry_blacksmith = models.IntegerField(default=1000_000_000)

	industry_animals = models.IntegerField(default=100_000_000)
	industry_vegetable = models.IntegerField(default=200_000_000)
	industry_wheat = models.IntegerField(default=300_000_000)

	industry_typography = models.IntegerField(default=50_000_000)

	industry_light = models.IntegerField(default=300_000_000)

	industry_eating = models.IntegerField(default=200_000_000)

	industry_jewelry = models.IntegerField(default=100_000_000)

	industry_transport = models.IntegerField(default=200_000_000)

	industry_alchemy = models.IntegerField(default=50_000_000)

	industry_hiring = models.IntegerField(default=300_000_000)

	industry_culture = models.IntegerField(default=100_000_000)

	industry_other = models.IntegerField(default=300_000_000)

	def get_gdp(self):
		attr = [a for a in dir(Regions) if a.startswith('industry')]
		summ = 0
		for i in attr:
			summ += getattr(self,i) 
		return summ

	# Needs of population
	needs_blackmetall = models.IntegerField(default=700_000_000)
	needs_colormetall = models.IntegerField(default=400_000_000)
	needs_coal = models.IntegerField(default=200_000_000)

	needs_hunting = models.IntegerField(default=300_000_000)
	needs_fishing = models.IntegerField(default=300_000_000)

	needs_forestry = models.IntegerField(default=500_000_000)

	needs_blacksmith = models.IntegerField(default=1000_000_000)

	needs_animals = models.IntegerField(default=100_000_000)
	needs_vegetable = models.IntegerField(default=200_000_000)
	needs_wheat = models.IntegerField(default=300_000_000)

	needs_typography = models.IntegerField(default=50_000_000)

	needs_light = models.IntegerField(default=300_000_000)

	needs_eating = models.IntegerField(default=200_000_000)

	needs_jewelry = models.IntegerField(default=100_000_000)

	needs_transport = models.IntegerField(default=200_000_000)

	needs_alchemy = models.IntegerField(default=50_000_000)

	needs_hiring = models.IntegerField(default=300_000_000)

	needs_culture = models.IntegerField(default=100_000_000)

	needs_other = models.IntegerField(default=300_000_000)

	def get_needs(self):
		attr = [a for a in dir(Regions) if a.startswith('needs')]
		summ = 0
		for i in attr:
			summ += getattr(self,i) 
		return summ

	def __str__(self):
		return self.name

	class Meta:
	    verbose_name = 'Default Регион'
	    verbose_name_plural = 'Default Регионы'

class Tax(models.Model):		
	tax_type = models.CharField(max_length=1, choices=[('j','Jure'),('p','Phys')], default='p')
	name = models.CharField(max_length=15, default='Default tax')
	status = models.CharField(max_length=1, choices=[('f','Federal'),('r','Regional')], default='f')
	value = models.FloatField(default=0.1)

	def __str__(self):
		return self.name + f' ({self.status.upper()}) : {int(self.value*100)}%'

	class Meta:
	    verbose_name = 'Default Налог'
	    verbose_name_plural = 'Default Налоги'

class Country(models.Model):
	# Main properties
	name = models.CharField(max_length=20, default='Default country', unique=True)
	regions = models.ManyToManyField(Regions)
	capital = models.OneToOneField(Regions, on_delete=models.CASCADE, related_name='region_capital', unique=True)
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

	def get_universities(self):
		summ = 0
		for i in self.regions.all():
			summ += i.universities
		return summ

	def get_schools(self):
		summ = 0
		for i in self.regions.all():
			summ += i.schools
		return summ

	def get_aqueducs(self):
		summ = 0
		for i in self.regions.all():
			summ += i.aqueducs
		return summ

	def get_stone_road(self):
		summ = 0
		for i in self.regions.all():
			summ += i.aqueducs
		return summ / len(self.regions.all())

	def get_pave_road(self):
		summ = 0
		for i in self.regions.all():
			summ += i.aqueducs
		return summ / len(self.regions.all())

	def get_poverty(self):
		summ = 0
		for i in self.regions.all():
			summ += i.poverty
		return summ / len(self.regions.all())

	def get_unemployment(self):
		summ = 0
		for i in self.regions.all():
			summ += i.unemployment
		return summ / len(self.regions.all())

	def get_avg_salary(self):
		summ = 0
		for i in self.regions.all():
			summ += i.avg_salary
		return summ / len(self.regions.all())

	# Industries of economy

	def get_industry_blackmetall(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_blackmetall
		return summ

	def get_industry_colormetall(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_colormetall
		return summ

	def get_industry_coal(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_coal
		return summ

	
	def get_industry_hunting(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_hunting
		return summ

	def get_industry_fishing(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_fishing
		return summ


	def get_industry_forestry(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_forestry
		return summ


	def get_industry_blacksmith(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_blacksmith
		return summ


	def get_industry_animals(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_animals
		return summ

	def get_industry_vegetable(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_vegetable
		return summ

	def get_industry_wheat(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_wheat
		return summ


	def get_industry_typography(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_typography
		return summ

	def get_industry_light(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_light
		return summ

	def get_industry_eating(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_eating
		return summ

	def get_industry_jewelry(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_jewelry
		return summ

	def get_industry_transport(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_transport
		return summ

	def get_industry_transport(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_transport
		return summ

	def get_industry_alchemy(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_alchemy
		return summ

	def get_industry_hiring(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_hiring
		return summ

	def get_industry_culture(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_culture
		return summ

	def get_industry_other(self):
		summ = 0
		for i in self.regions.all():
			summ += i.industry_other
		return summ

	# Needs of economy

	def get_needs_blackmetall(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_blackmetall
		return summ

	def get_needs_colormetall(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_colormetall
		return summ

	def get_needs_coal(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_coal
		return summ

	
	def get_needs_hunting(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_hunting
		return summ

	def get_needs_fishing(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_fishing
		return summ


	def get_needs_forestry(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_forestry
		return summ


	def get_needs_blacksmith(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_blacksmith
		return summ


	def get_needs_animals(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_animals
		return summ

	def get_needs_vegetable(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_vegetable
		return summ

	def get_needs_wheat(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_wheat
		return summ
	 

	def get_needs_typography(self):
		summ = 0
		for i in self.regions.all():
			summ += i.typography
		return summ

	def get_needs_light(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_light
		return summ

	def get_needs_eating(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_eating
		return summ

	def get_needs_jewelry(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_jewelry
		return summ

	def get_needs_transport(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_transport
		return summ

	def get_needs_transport(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_transport
		return summ

	def get_needs_alchemy(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_alchemy
		return summ

	def get_needs_hiring(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_hiring
		return summ

	def get_needs_culture(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_culture
		return summ

	def get_needs_other(self):
		summ = 0
		for i in self.regions.all():
			summ += i.needs_other
		return summ

	def get_gdp(self):
		attr = [func for func in dir(Country) if callable(getattr(Country, func)) and func.startswith('get_industry')]
		summ = 0
		for i in attr:
			summ += getattr(self,i)()
		return summ

	def get_needs(self):
		attr = [a() for a in dir(Country) if a.startswith('get_needs')]
		summ = 0
		for i in attr:
			summ += getattr(self,i) 
		return summ

	def get_infrastructure(self):
		summ = 0
		for i in self.regions.all():
			summ += i.infrastructure
		return summ / len(self.regions.all())

	def get_port(self):
		summ = 0
		for i in self.regions.filter(port=True):
			summ += i.port
		return summ / len(self.regions.filter(port=True))

	def get_cargo_ship(self):
		summ = 0
		for i in self.regions.all():
			summ += i.cargo_ship
		return summ / len(self.regions.all())

	def get_people_ship(self):
		summ = 0
		for i in self.regions.all():
			summ += i.people_ship
		return summ / len(self.regions.all())

	education_quality = models.FloatField(default=0.6)
	education_avail = models.FloatField(default=0.6)
	alchemy = models.FloatField(default=0.6)
	magic = models.FloatField(default=0.6) 
	science = models.FloatField(default=0.6)
	technology = models.FloatField(default=0.6)
	export_trash = models.FloatField(default=0.6)

	def get_panteon_daedra(self):
		return 1.0 - self.panteon_eight - self.panteon_nine

	support = models.FloatField(default=0.6)
	stability = models.FloatField(default=0.6)

	government = models.CharField(max_length=7, default='m,t,a,p') # m(M-monarchy,O-parlament monarchy,D-dictator,R-republic), t(0,1 other), a(0,1 other), p(0,1 other)
	area_format = models.CharField(max_length=7, default='c,p,l,e') # c(C-centraliz, D-decentraliz), p(S-svobod, O-ogranich, Z-zaprech), l(M-mestnaya, F-feder), e(I-izbir, N-naznach)

	army_salary = models.CharField(max_length=13, default='2,1600,2500') # 2(vyhod pencia(1-40,2-45,3-50,4-60)), 1600(avg z/p), 2500(avg pensia)
	army_maintain = models.CharField(max_length=5, default='2,1,3') # 2(pytanye(1-no,2-min,3-avg,4-max)), 1(infrastruc(1-min,2-avg,3-max)), 3(bytovye usloviya(1-min,2-avg,3-max))
	army_equip = models.CharField(max_length=5, default='4,3,1') # 4(equip(1-kozhanay,2-iron,3-lamelar,4-orikhalk,5-ebonyt)), 3(komplect(1-1,2-1.5,3-2,4-3)), 1(resursi(1-min,2-avg,3-max))

	maternal_capital = models.IntegerField(default=5000)
	avg_pension = models.IntegerField(default=1500)
	allowance_unemploy = models.IntegerField(default=500)
	allowance_disability = models.IntegerField(default=500)

	pension_m = models.CharField(max_length=1, default='3') # 1(50),2(55),3(60),4(65)
	pension_w = models.CharField(max_length=1, default='2') # 1(45),2(50),3(55),4(60)

	inflation = models.FloatField(default=5.5)

	taxes = models.ManyToManyField(Tax, blank=True) 

	law_equal_rights = models.BooleanField(default=True)
	law_torture = models.BooleanField(default=True)
	law_speech = models.BooleanField(default=True)
	law_demonstration = models.BooleanField(default=True)
	law_property = models.BooleanField(default=True)
	law_creation = models.BooleanField(default=True)
	law_rasism = models.BooleanField(default=True)
	law_heritage = models.BooleanField(default=True)
	law_slavery = models.BooleanField(default=True)
	law_court = models.BooleanField(default=True)
	law_child_labour = models.BooleanField(default=True)
	law_monopoly = models.BooleanField(default=True)
	law_free_enterspire = models.BooleanField(default=True)
	law_work_day_limit = models.BooleanField(default=True)
	law_death_penalty = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	class Meta:
	    verbose_name = 'Default Страна'
	    verbose_name_plural = 'Default Страны'

class Relations(models.Model):	
	pair = models.ManyToManyField(Country)
	value = models.IntegerField(default=0)

	def __str__(self):
		return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + str(self.value)

	class Meta:
	    verbose_name = 'Default Отношение'
	    verbose_name_plural = 'Default Отношения'

class Contracts(models.Model):		
	pair = models.ManyToManyField(Country)
	
	YEAR_IN_SCHOOL_CHOICES = [
        ('AL', 'Alliance'),
        ('CM', 'Common market'),
        ('CT', 'Culture transfer'),
        ('SH', 'Social help'),
        ('EH', 'Economic help'),
        ('PA', 'Passage of army'),
        ('ES', 'Economic sanctions'),
        ('DW', 'Declare war'),
		('CP', 'Contract of Peace'),
		('FW', 'Finish war'),
    ]
    
	con_type = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default='EH')

	def __str__(self):
		return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + self.con_type

	class Meta:
	    verbose_name = 'Default Договор'
	    verbose_name_plural = 'Default Договора'

class Squad(models.Model):
	pechot_quan = models.IntegerField(default=100)
	archer_quan = models.IntegerField(default=100)
	cavallery_quan = models.IntegerField(default=100)

	catapult_quan = models.IntegerField(default=10)

	esmin_quan = models.IntegerField(default=10)
	linkor_quan = models.IntegerField(default=10)

	place_type = models.CharField(max_length=1, choices=[('G', 'Ground'),('S', 'Sea')], default='G')

	country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)

	status = models.CharField(max_length=1, choices=[('R', 'Ready'),('Q', 'Quartered')], default='Q')

	def summ(self):
		final = self.pechot_quan + self.archer_quan + self.cavallery_quan + self.catapult_quan*5 +\
		self.esmin_quan*100 + self.linkor_quan*400
		
		return final

	def __str__(self):
		return self.country.name + ' : ' + str(self.summ())

	class Meta:
	    verbose_name = 'Default Отряд'
	    verbose_name_plural = 'Default Отряды'