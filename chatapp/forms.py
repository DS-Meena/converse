# creating a form for user handle and user room
from django import forms

class quickForm(forms.Form):
	user_handle = forms.CharField(label='User handle', max_length=100)
	
	room = forms.CharField(label='Room name', max_length=100)