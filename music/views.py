from django.shortcuts import render
from django.views import View


class Music(View):

    def get(self, request):
        return render(request, 'music/music.html')

    def post(self, request):
        pass

    def delete(self, request):
        pass

    def put(self, request):
        pass
