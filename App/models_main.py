from django.db import models
from App.models_abstract import Abstract_Regions, Abstract_Country, Abstract_Contracts, Abstract_Relations, Abstract_Squad

class Regions(Abstract_Regions):

	def get_gdp(self):
		attr = [a for a in dir(Regions) if a.startswith('industry')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def get_needs(self):
		attr = [a for a in dir(Regions) if a.startswith('needs')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Default Регион'
		verbose_name_plural = 'Default Регионы'

class Country(Abstract_Country):
	regions = models.ManyToManyField(Regions)
	capital = models.OneToOneField(Regions, on_delete=models.CASCADE, related_name='region_capital',unique=True)

	def get_gdp(self):
		attr = [func for func in dir(Country) if
				callable(getattr(Country, func)) and func.startswith('get_industry')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)()
		return summ

	def get_needs(self):
		attr = [a() for a in dir(Country) if a.startswith('get_needs')]
		summ = 0
		for i in attr:
			summ += getattr(self, i)
		return summ

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Default Страна'
		verbose_name_plural = 'Default Страны'

class Relations(Abstract_Relations):

	pair = models.ManyToManyField(Country)

	def __str__(self):
		if len(self.pair.all()) == 2:
			return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + str(self.value)
		else:
			return 'Relation :' + str(self.value)

	class Meta:
		verbose_name = 'Default Отношение'
		verbose_name_plural = 'Default Отношения'

class Contracts(Abstract_Contracts):

	pair = models.ManyToManyField(Country)

	def __str__(self):
		return self.pair.all()[0].name + '-' + self.pair.all()[1].name + ' : ' + self.con_type

	class Meta:
		verbose_name = 'Default Договор'
		verbose_name_plural = 'Default Договора'

class Squad(Abstract_Squad):

	country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return self.country.name + ' : ' + str(self.summ())

	class Meta:
		verbose_name = 'Default Отряд'
		verbose_name_plural = 'Default Отряды'