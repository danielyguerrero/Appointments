from __future__ import unicode_literals
from ..login.models import User
from django.db import models
from datetime import datetime


#======================================================================
#+++++++++++++               MANAGER                 ++++++++++++++++++
#======================================================================

class AppointmentsManager(models.Manager):

#======================================================================
#                            APPOINTMENT VALIDATION
#======================================================================

	def validate(self, form_data):

		errors = []

		if len(form_data['tasks']) == 0 :

			errors.append("Must include an appointment task.")

		return errors

#======================================================================
#                            ADD APPOINTMENT
#======================================================================

	def addAppointment(self, form_data, user_id):

		tasks = form_data['tasks']

		status = form_data['status']

		time = form_data['time']

		date = form_data['date']

		user = User.objects.get(id=user_id)

		appointed_by = user

		self.create(tasks=tasks, status=status, time=time, date=date, appointed_by=user)


#======================================================================
#+++++++++++++               CLASS                   ++++++++++++++++++
#======================================================================

class Appointments(models.Model):

	tasks = models.CharField(max_length=150)

	status = models.CharField(max_length=150)

	time = models.TimeField(null=True, blank=True)

	date = models.DateField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)
	
	appointed_by = models.ForeignKey(User, null=True, related_name="appointments")

	objects = AppointmentsManager()

	def __str__(self):
		return "tasks: " + str(self.tasks) + ", status: " + self.status, "time:" + str(self.time)
