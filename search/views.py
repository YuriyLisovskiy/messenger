from django.http import JsonResponse
from django.views.generic import View

from account.models import UserProfile
from utils.view_modifiers import auth_required


class SearchPeople(View):

#	@auth_required
	def get(self, request):
		if 'search' in request.GET:
			keyword = request.GET.get('search')
			if 'city' in request.GET:
				f_n, l_n = keyword.split()
				filter_data = {
					'first_name': f_n,
					'last_name': l_n,
					'mobile_number': request.GET.get('mobile_number')
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
				'status': 'OK'
			}
		else:
			response = {
				'data': [x.to_dict() for x in UserProfile.get_all()],
				'status': 'OK'
			}
		return JsonResponse(response, status=200, safe=False)
