from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from asgiref.sync import async_to_sync

# Create your views here.

# DEBUG = False

# def my_room(request, roomName):
# 	context = {}
# 	context['debug_mode'] = settings.DEBUG
# 	context['debug'] = DEBUG
# 	context['roomName'] = roomName
# 	return render(request, "room/room.html", context)


def room(request, room_name):
    return render(request, 'room/room.html', {
        'room_name': room_name
    })