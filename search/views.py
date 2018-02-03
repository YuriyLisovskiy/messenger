from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from account.models import UserProfile
from utils.view_modifiers import auth_required


class SearchPeople(View):
	
	template_name = 'search/search.html'

	@auth_required
	def get(self, request):
		context = {
			'all_users': UserProfile.get_all()
		}
		return render(request, self.template_name, context=context)

	@auth_required
	def post(self, request):
		keyword = request.POST.get('search')
		if 'city' in request.POST:
			f_n, l_n = keyword.split()
			filter_data = {
				'first_name': f_n,
				'last_name': l_n,
				'city': request.POST.get('city'),
				'country': request.POST.get('country'),
				'birthday': request.POST.get('birthday'),
				'gender': request.POST.get('gender')
			}
			user_profiles = UserProfile.filter_by(**filter_data)
		elif " " in keyword:
			f_n, l_n = keyword.split()
			filter_data = {
				'first_name__icontains': f_n,
				'last_name__icontains': l_n
			}
			user_profiles = UserProfile.filter_by(**filter_data)
		else:
			first_name_data = {
				'first_name__icontains': keyword
			}
			last_name_data = {
				'last_name__icontains': keyword
			}
			user_profiles = UserProfile.filter_by(**first_name_data) | UserProfile.filter_by(**last_name_data)
		response = {
			'data': [user_profile.to_dict() for user_profile in user_profiles],
			'status': 'CREATED'
		}
		return JsonResponse(response, safe=False)
