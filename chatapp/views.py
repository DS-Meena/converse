from django.shortcuts import render
from django.conf import settings

# Create your views here.

# try to render the form also
from .forms import quickForm

# lets try to access the room names
from room.utils import myDict as authDict
from quickchat.utils import myDict as unauthDict

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

	print("THE AUTH DICT IS LIKE THIS", authDict)
	print("THE UNAUTH DICT IS LIKE THIS", unauthDict)

	# tuple of room name and active users count
	context['rooms'] = []
	# send the room names also
	if request.user.is_authenticated:
		# tuple of room name and no of users in it
		for key in list(authDict.keys()):
			context['rooms'].append((key, len(authDict[key])))
	else:
		# tuple of room name and no of users in it
		for key in list(unauthDict.keys()):
			context['rooms'].append((key, len(unauthDict[key])))

	print("details about chatrooms:", context['rooms'])

	return render(request, "chatapp/home.html", context)