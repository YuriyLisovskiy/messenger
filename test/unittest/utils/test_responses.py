from django.test import TestCase, RequestFactory

from utils.responses import BAD_REQUEST, NOT_FOUND, PERMISSION_DENIED


class TestResponses(TestCase):
	
	def setUp(self):
		self.factory = RequestFactory()
	
	def test_bad_request(self):
		response = BAD_REQUEST
		self.assertEqual(response.status_code, 400)
		
	def test_permission_denied(self):
		response = PERMISSION_DENIED
		self.assertEqual(response.status_code, 403)
	
	def test_not_found(self):
		response = NOT_FOUND
		self.assertEqual(response.status_code, 404)
