from django.shortcuts import render
from django.conf import settings

# Create your views here.

# try to render the form also
from .forms import quickForm

def home_screen_view(request):
	context = {}
	form = quickForm(request.POST)
	
	# if form is filled and we click submit querey then
	if form.is_valid():
		user_handle = form.cleaned_data['user_handle']
		room = form.cleaned_data['room']

		print(room)
		print(user_handle)

		# go to quick chat room
		return render(request, 'quickchat/room.html', {
        'room_name': room,
        'userhandle': user_handle
    })


	context['debug_mode'] = settings.DEBUG
	context['room_id'] = "1"
	# render the quickform in form variable
	context['form'] = quickForm
	return render(request, "chatapp/home.html", context)