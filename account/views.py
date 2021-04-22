from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
# got user account page 
from django.conf import settings

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

# get model for user account page
from account.models import Account
from django.db.models import Q
# these views are related to the user management functionality
# to register a new user

# To fetch friendlist
from friends.friend_request_status import FriendRequestStatus
from friends.models import FriendList,FriendRequest

# To fetch Bloglist
from blogs.models import Post

# To get friend req state
from friends.utils import get_friend_request_or_false


# This is basically almost exactly the same as friends/friend_list_view
def account_search_view(request, *args, **kwargs):
	# I THINK THE PROBLEM IS HERE 
	# OF THE SHOWING NOT FRIENDS IN SEARCH RESULTS
	context = {}

	if request.method == "GET":
		# get the search query
		search_query = request.GET.get("q")
		# atleast one character
		if len(search_query) > 0:
			# get the search results
			# YAHAN PE DEKH SEARCH QUERY IDHAR SE SAHI RESULTS FILTER KAREGI
			search_results = Account.objects.filter(Q(email__icontains=search_query)|Q(username__startswith=search_query)).distinct()
			
			print("search results are", search_results)
			user = request.user
			accounts = []  # [(account1, True), (account2, False), ...]
			
			if user.is_authenticated:
				# get the authenticated users friend list

				auth_user_friend_list = FriendList.objects.get(user=user)
				
				# for each account
				for account in search_results:
					accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
					
				context['accounts'] = accounts
				
				# trying to add all friends 
				# context['myfriends'] = auth_user_friend_list 

			# all are authenticated
			else:
				for account in search_results:
					accounts.append((account, True))
				context['accounts'] = accounts

	print("so see friends", context)
	return render(request, "account/search_results.html", context)

# to search users (placed on header)
# where this comes from (kha s aa gaya) (due to this it shows not friend)
# def account_search_view(request, *args, **kwargs):
# 	context = {}
# 	if request.method == "GET":
# 		search_query = request.GET.get("q")
# 		if len(search_query) > 0:
# 			search_results = Account.objects.filter(Q(username__icontains=search_query)|Q(email__icontains=search_query)).distinct()
# 			user = request.user
# 			print(search_results)
# 			accounts = [] # [(account1, True), (account2, False), ...]
# 			for account in search_results:
# 				accounts.append((account, False)) # you have no friends yet
# 			context['accounts'] = accounts
				
# 	return render(request, "account/search_results.html", context)

def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

# to logout user
def logout_view(request):
	logout(request)
	return redirect("home")

# to login user
def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "account/login.html", context)

# redirect to next page
def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

# to go to user account section
def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

	# Account's Friend List Section Logic
		try:
			# if friend list exist on user profile
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			# if it doesn't exist then we need to create it
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends

	# Account's Blog list Section Logic
		try:
			# if blogs exist on user profile
			blog_list = Post.objects.filter(author=account)
			print(blog_list)
		except Post.DoesNotExist:
			pass
			# if it doesn't exist then we need need to create it
			
		context['blogs']= blog_list

		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		# range : ENUM-> friends/friend_request_status.FriendRequestStatus
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend =True
			else :
				is_friend=False
				# Case 1 : req has been sent from them to user
				# FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender=account, receiver=user)!=False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(
						sender=account, receiver=user).id

				#Case 2: req has been sent from you to them
				elif get_friend_request_or_false(sender=account, receiver=user)!=False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# Case 3 : No request has been sent, FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent =FriendRequestStatus.NO_REQUEST_SENT.value
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass

		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		return render(request, "account/account.html", context)


# to edit account details method
def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			new_username = form.cleaned_data['username']
			return redirect("account:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "account/edit_account.html", context)
