from django.shortcuts import render
from django.conf import settings

# Create your views here.

# def my_chatroom(request, room_name):
#     return render(request, "chatroom/my_chatroom.html", {
#     	'room_name' : room_name
#     	})

DEBUG = False

def my_chatroom(request, room_name):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_name'] = room_name
	return render(request, "chatroom/my_chatroom.html", context)