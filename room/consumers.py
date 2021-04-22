import json
from channels.generic.websocket import AsyncWebsocketConsumer

# to calcualte the timestamp
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.utils import timezone
from datetime import datetime

# to get user details
from django.contrib.auth import get_user_model
User = get_user_model()

# import the dictionary that we have created 
# to store connected users and chatroom name
from room.utils import *

# get the accounts and friends
from account.models import Account


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # add this person in that dictionary
        print("we have this", myDict)

        # add the like this ["room_name"] = [username all]
        # if first one to enter (create key)
        # CHANGE - Store the user id also
        if self.room_name not in myDict.keys(): 
            myDict[self.room_name] = [[self.scope['user'].username, self.scope['user'].id]]
        else:
            myDict[self.room_name].append([self.scope['user'].username, self.scope['user'].id])

        print("now we have", myDict)
        print_dic()

        # writing the python dict into a json
        # send_dict = json.dumps(myDict)

        # define first then call
        # find_accounts(self)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # if new user joinss 
        # send message to group and also add to connected user list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                # new user joins
                'message': 'connected',
                'update_list': True,

                # trying to use user model
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
            }
        )

        # Send message to WebSocket
        # await self.send(text_data=json.dumps({
        #     'update_list': True,
        #     'connected_users': myDict[self.room_group_name],
        # }))

    async def disconnect(self, close_code):
        # Leave room group

        print("now we have", myDict)

        # if user is leaving remov it from connected users list
        myDict[self.room_name].remove([self.scope['user'].username, self.scope['user'].id])

        print("now we have", myDict)
        print_dic()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # if user leaves 
        # send message to group and also remove from connected user list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                # new user joins
                'message': 'Disconnected',
                'update_list': True,

                # trying to use user model
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # trying send_room functions 
        # get sending response using send_room function
        if len(message.lstrip()) != 0: # not send empty messages
            await self.send_room(message)

        # Send message to room group
        # neche laga diya

    # send room function to call chat message function
    async def send_room(self, message):

        # call chat message which will send the message to group
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'update_list': False,

                # trying to use user model
                'username': self.scope['user'].username,
                'user_id': self.scope['user'].id,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # try to calcualte the timestamp also
        timestamp = calculate_timestamp(timezone.now())

        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': event['username'],
            'user_id': event['user_id'],
            'natural_timestamp': timestamp,

            # details about connected users list
            'update_list': event['update_list'],

            # CHANGE - now the list is a tuple of (name, id)
            'connected_users': myDict[self.room_name],
        }))

# this function will get the time at which message sent
def calculate_timestamp(timestamp):
    """
    1. Today or yesterday:
        - EX: 'today at 10:56 AM'
        - EX: 'yesterday at 5:19 PM'
    2. other:
        - EX: 05/06/2020
        - EX: 12/28/2020
    """
    ts = ""
    # Today or yesterday
    if (naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday"):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    # other days
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    return str(ts)