from django.shortcuts import render, get_object_or_404, redirect, reverse
from . models import Album, Song
from . forms import AlbumForm, SongForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView


# Create your views here
def index(request):
	albums = Album.objects.all()
	return render(request, 'musicapp/index.html', {'albums': albums})


def detail(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	return render(request, 'musicapp/detail.html', {'album': album})


class AlbumUpdateView(UpdateView):
	model = Album
	fields = ['name', 'artist', 'genre', 'cover']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		album = self.get_object()
		if self.request.user == album.user:
			return True
		return False


@login_required(login_url='musicapp:login_user')
def create_album(request):
	form = AlbumForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		album = form.save(commit=False)
		album.cover = request.FILES['cover']
		album.user = request.user
		album.save()
		return render(request, 'musicapp/detail.html', {'album': album})
	form = AlbumForm()
	return render(request, 'musicapp/create_album.html', {'form': form})


@login_required(login_url='musicapp:login_user')
def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		for s in album.song_set.all():
			if s.song_name == form.cleaned_data.get('song_name'):
				context = {'form': form,
						   'message': 'Already Added that song!'
						   }
				return render(request, 'musicapp/create_song.html', context)
		song = form.save(commit=False)
		song.album = album
		song.song_file = request.FILES['song_file']
		song.save()
		context = {'album': album,
				   'message': 'Song Added!'
				   }
		return render(request, 'musicapp/detail.html', context)
	form = SongForm()
	return render(request, 'musicapp/create_song.html', {'form': form})


def delete_album(request, album_id):
	album = Album.objects.get(pk=album_id)
	album.delete()
	albums = Album.objects.all()
	return render(request, 'musicapp/index.html', {'albums': albums})


class SongUpdateView(UpdateView):
	model = Song
	fields = ['song_name', 'song_file']

	def get_absolute_url(self):
		return reverse('musicapp:detail')

	def form_valid(self, form):
		return super().form_valid(form)


def delete_song(request, album_id, song_id):
	album = get_object_or_404(Album, pk=album_id)
	song = get_object_or_404(album.song_set, pk=song_id)
	song.delete()
	context = {'album': album,
			   'message': 'Song Deleted!'
			   }
	return render(request, 'musicapp/detail.html', context)


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
				albums = Album.objects.filter(user=request.user)
				return render(request, 'musicapp/index.html', {'albums': albums})
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
	return redirect('musicapp:login_user')









