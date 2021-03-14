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

def quickchat(request, room_name):

    return render(request, 'quickchat/room.html', {
        'room_name': room_name,
        'userhandle': user_handle
    })


# def withForm(request):
# 	form = quickForm(request.POST)

# 	return render(request, 'quickchat/room.html', {
# 			'room_name': form.cleaned_data['room'],
# 			'userhandle': form.cleaned_data['user_handle']
# 		})
