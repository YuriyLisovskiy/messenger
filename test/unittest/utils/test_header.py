from django.test import TestCase

from utils.header import COUNTRY_LIST


class TestHeader(TestCase):
	
	def test_get_iso_code(self):
		self.assertEqual(COUNTRY_LIST.get_iso_code('Ukraine'), 'UA')
	
	def test_get_county(self):
		self.assertEqual(COUNTRY_LIST.get_county('WF'), 'Wallis and Futuna')
	
	def test_country_list(self):
		self.assertEqual(len(COUNTRY_LIST.country_list()), 249)
