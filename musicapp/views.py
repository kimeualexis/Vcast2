from django.shortcuts import render, get_object_or_404, redirect
from . models import Album
from . forms import AlbumForm, SongForm, UserForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def index(request):
	albums = Album.objects.all()
	return render(request, 'musicapp/index.html', {'albums': albums})


def detail(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	return render(request, 'musicapp/detail.html', {'album': album})


def create_album(request):
	form = AlbumForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		album = form.save(commit=False)
		album.cover = request.FILES['cover']
		album.save()
		return render(request, 'musicapp/detail.html', {'album': album})
	form = AlbumForm()
	return render(request, 'musicapp/create_album.html', {'form': form})


def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		song = form.save(commit=False)
		song.album = album
		song.song_file = request.FILES['song_file']
		song.save()
		return render(request, 'musicapp/detail.html', {'album': album})
	form = SongForm()
	return render(request, 'musicapp/create_song.html', {'form': form})


def delete_album(request, album_id):
	album = Album.objects.get(pk=album_id)
	album.delete()
	albums = Album.objects.all()
	return render(request, 'musicapp/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
	album = get_object_or_404(Album, pk=album_id)
	song = get_object_or_404(album.song_set, pk=song_id)
	song.delete()
	return render(request, 'musicapp/detail.html', {'album': album})


def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('musicapp:index')
	form = UserForm()
	return render(request, 'musicapp/register.html', {'form': form})


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('musicapp:index')
	return render(request, 'musicapp/login.html')


def logout_user(request):
	logout(request)
	return redirect('musicapp:index')









