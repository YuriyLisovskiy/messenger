from django.test import TestCase

from utils.functions import check_password


class TestFunctions(TestCase):

	def test_check_password(self):
		self.assertEqual(check_password('123456qwerty'), True)
		self.assertEqual(check_password('12345'), False)
