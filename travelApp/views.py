from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import datetime
from django.db.models import Q


# Create your views here.
def index(request):
	# passthrough to login
	return redirect("/main")

def login(request):
	# displays login and registration page
	return render(request, "index.html")

def loginUser(request):
	usernameMatch = User.objects.filter(username = request.POST['loginUsername'])
	errors = User.objects.loginValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	if usernameMatch:
		logged_user = usernameMatch[0]
		if bcrypt.checkpw(request.POST['loginPassword'].encode(), logged_user.password.encode()):
			request.session['loggedInUserID'] = logged_user.id
			return redirect('/travels')

def logoutUser(request):
	# clears session logging user out
	request.session.clear()
	return redirect('/')

def register(request):
	# creates new user object after data validation
	errors = User.objects.regValidate(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password =request.POST['password']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		newUser = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = pw_hash)
		request.session['loggedInUserID'] = newUser.id
		return redirect('/travels')

def alltravel(request):
	# home page after login
	user =  User.objects.get(id = request.session['loggedInUserID'])
	availableTrip = Trip.objects.exclude(Q(joiner = user) | Q(creator = user))
	context ={
	"user" : user,
	'trips' : Trip.objects.all(),
	'userTrips' : (Trip.objects.filter(joiner = user) | Trip.objects.filter(creator = user)),
	'availableTrip' : availableTrip
	}
	return render(request, "home.html", context)

def addtravel(request):
	#directs to the add travel page
	return render(request,"addtrip.html")

def submitTravel(request):
	#validates trip data submission and creates trip object
	errors = User.objects.tripValidate(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/travels/add')
	else:
		# default = User.objects.get(id = 1)
		print(request.POST['startDate'])
		user =  User.objects.get(id = request.session['loggedInUserID'])
		newtrip = Trip.objects.create(destination = request.POST['destination'], startDate = request.POST['startDate'], endDate = request.POST['endDate'], description = request.POST['description'], creator = user)
		newtrip.joiner.add(user)
		return redirect('/travels')

def tripInfo(request, tripID):
	# display trip information
	context ={
		"trip" : Trip.objects.get(id = tripID)
	}
	
	return render(request,"trip.html", context)

def joinTrip(request, joinID):
	trip = Trip.objects.get(id = joinID)
	trip.joiner.add(User.objects.get(id = request.session['loggedInUserID']))
	return redirect('/travels')