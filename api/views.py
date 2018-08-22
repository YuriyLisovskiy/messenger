from django.views import View
from django.shortcuts import render

from utils.responses import BAD_REQUEST


class IndexView(View):
	template_name = 'home.html'

	def get(self, request):
		return render(request, self.template_name)

	@staticmethod
	def post():
		return BAD_REQUEST
