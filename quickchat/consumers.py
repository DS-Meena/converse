import json
from channels.generic.websocket import AsyncWebsocketConsumer

# to calcualte the timestamp
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.utils import timezone
from datetime import datetime

# trying using form
from chatapp.forms import quickForm

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
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
        # idhar access karna chata hu form
        # taki return kar saku room.html ko
        # par no request so no response
        # form = quickForm()
        # if form.is_valid():
        #     user_handle = user_handle = form.cleaned_data['user_handle']
        # else:
        #     user_handle = "unknown"
        # print(user_handle)

        # call chat message which will send the message to group
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                # trying to get user handle
                'username': 'unknown',
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # try to get user handle from text box
        

        # try to calcualte the timestamp also
        timestamp = calculate_timestamp(timezone.now())

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': event['username'],

            'natural_timestamp': timestamp,
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