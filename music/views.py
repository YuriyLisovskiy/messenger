from django.shortcuts import render
from django.views import View
from .models import Song


class Music(View):

    def get(self, request):
        songs = Song.objects.all()
        context = {'songs': songs}
        return render(request, 'music/music.html', context)

    def post(self, request):
        pass

    def delete(self, request):
        pass

    def put(self, request):
        pass


class MusicManager(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass
