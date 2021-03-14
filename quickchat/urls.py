from django.urls import path

from quickchat.views import (
	quickchat,
	# withForm,
)

app_name = 'quickchat'

urlpatterns = [
    path('<str:room_name>/', quickchat, name='quickchat'),
    # path('/',withForm, name='withForm')
]