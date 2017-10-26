from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors =[]

        if len(form_data['name']) == 0:
            errors.append("First Name is required.")

        if len(form_data['alias']) == 0:
            errors.append("Last Name is required.")
      
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
      
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
       
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("Passwords must match.")

        if not errors:
            user = User.objects.filter(email=form_data['email'].lower()).first()
            if user:
                errors.append("Email already taken")

        return errors



    def validate_login(self, form_data):
        errors = []
       
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
       
        if len(form_data['password']) == 0:
            errors.append("Password is required.")

        if not errors:
            user = User.objects.filter(email=form_data['email'].lower()).first()
            if user:
                user_password = form_data['password'].encode()
                db_password = user.password.encode()

                if bcrypt.checkpw(user_password, db_password):
                    return {'user': user}

        errors.append("Login failed")
        return {'errors': errors}

    def create_user(self, form_data):
        hashedpw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())

        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'].lower(),
            password = hashedpw,
    )

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
