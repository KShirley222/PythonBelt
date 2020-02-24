from django.db import models
import re
import bcrypt
import datetimecode
class UserManager(models.Manager):
	# registration validator
	def regValidate(self, postData):
		errors = {}
		usernameMatch = User.objects.filter(username = postData['username'])
		if len(postData['name']) < 3:
			errors['reqName'] = "Name is required and must be 3 or more characters."
		if len(postData['username']) < 3:
			errors['reqUsername'] = "Alias is required and must be 3 or more characters."
		if len(postData['password']) < 8:
			errors["PW_short"] = "Password should be at least 8 characters"
		if postData['password'] != postData['confirmPw']:
			errors["PW_no_match"] = "Passwords must match"
		if len(usernameMatch) > 0:
			errors['usernameUnav'] = 'This username is already in used.'
		return errors

	def loginValidator(self,postData):
		errors = {}
		if len(postData['loginUsername'])<1:
			errors['email_required'] = "Username required to login"
		usernameMatch = User.objects.filter(username = postData['loginUsername'])
		if len(usernameMatch) == 0:
			errors['no_email'] = 'No username found.'
		else:
			user = usernameMatch[0]	
			if bcrypt.checkpw(postData['loginPassword'].encode(), user.password.encode()):
				print("password Matches")
			else:
				errors['try_again'] = "Password incorrect"
		return errors

	def tripValidate(self,postData):
		errors = {}
		currentDate = datetime.datetime.now()
		if len(postData['destination']) < 1:
			errors['reqDestination'] = "Destination is required."
		if len(postData['description']) < 1:
			errors['reqDesc'] = "Trip Description is required."
		if postData['startDate'] != '':
			startDate = datetime.datetime.strptime(postData['startDate'],"%Y-%m-%d")
		else:
			errors['reqSD'] = 'Start Date is required.'
		if postData['endDate'] != '':
			endDate = datetime.datetime.strptime(postData['endDate'],"%Y-%m-%d")
		else:
			errors['reqED'] = 'End Date is required.'
		if postData['startDate'] != '' and postData['endDate'] != '':
			if startDate < currentDate:
				errors['earlySD'] = 'Start date must be in the future.'
			if endDate < startDate:
				errors['dateBefore'] = 'End date must be after start date'
		
		return errors
		

# TODAY_CHECK = datetime.datetime.now()
# start = datetime.datetime.strptime("26-11-2017", "%d-%m-%Y")
# end = datetime.datetime.strptime("30-11-2017", "%d-%m-%Y")


# Create your models here.
class User(models.Model):
	name =  models.CharField(max_length=255)
	username =  models.CharField(max_length=255)
	password =  models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


class Trip(models.Model):
	destination =  models.CharField(max_length=255)
	startDate = models.DateField()
	endDate = models.DateField()
	description = models.TextField()
	joiner = models.ManyToManyField(User, related_name="joined")
	creator = models.ForeignKey(User, related_name="creator", on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()