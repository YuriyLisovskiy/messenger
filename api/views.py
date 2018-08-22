from django.views import View
from django.shortcuts import render

from utils.responses import BAD_REQUEST


class IndexView(View):
	template_name = 'home.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		return BAD_REQUEST
