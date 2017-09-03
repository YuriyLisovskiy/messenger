from django.shortcuts import render, redirect
from django.views import View
from .models import Song, Album
from chat.models import UserProfile
from .serializers import SongSerializer
from django.http import JsonResponse


class Music(View):

    def get(self, request):
        songs = Song.objects.filter(owner__username=request.user.username)
        albums = Album.objects.filter(owner__username=request.user.username)
        context = {
            'songs': songs,
            'albums': albums
        }
        return render(request, 'music/music.html', context)

    def post(self, request):
        owner = UserProfile.objects.get(id=request.user.id)
        title = request.POST['title']
        artist = request.POST['artist']
        logo = request.FILES['logo']
        if request.POST['description'] != "":
            description = request.POST['description']
        else:
            description = ""
        new_album = Album(
            owner=owner,
            title=title,
            artist=artist,
            logo=logo,
            description=description
        )
        new_album.save()
        return redirect('music')

    def delete(self, request):
        pass

    def put(self, request):
        pass


class MusicManager(View):

    def get(self, request):
        try:
            songs = Song.objects.filter(album__id=request.GET['album_id'])
            serializer = SongSerializer(songs, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Song.DoesNotExist:
            return JsonResponse({'error': 'Play list of this album is empty.'})

    def post(self, request):
        pass

    def delete(self, request):
        pass
