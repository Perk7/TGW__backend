from django.test import TestCase
from .models_main import Country

class YourTestClass(TestCase):

    @classmethod
    def setUp(self):
        # Установки запускаются перед каждым тестом
        pass

    def tearDown(self):
        # Очистка после каждого метода
        pass

    def test_something_that_will_pass(self):
        pass

    def test_something_that_will_fail(self):
        self.client.get('/excel')
        countries = Country.objects.all()
        print(countries)
        self.assertTrue(len(countries) == 21)
