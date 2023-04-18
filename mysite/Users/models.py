from django.db import models
from Employees.models import Employees
import hashlib
from django.core.exceptions import ValidationError
# Create your models here.
#Users model
class Users(models.Model):
    # Define employee_id as a foreign key to the Employees model,
    # and set the on_delete behavior to cascade (delete all related records)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    # Define isActive as a Boolean field with a default value of True
    isActive = models.BooleanField(default=True)
    # Define useraccess as a character field with a maximum length of 255
    useraccess = models.CharField(max_length=255)
    # Define passphrase as a character field with a maximum length of 255
    passphrase = models.CharField(max_length=255)
    # Define salt as a character field with a maximum length of 255
    salt = models.CharField(max_length=255)
    # Define created_by as a character field with a maximum length of 255
    created_by = models.CharField(max_length=255)
    # Define created_datetime as a date/time field that automatically records the date/time
    # when the record is created
    created_datetime = models.DateTimeField(auto_now_add=True)
    # Define Meta class to provide additional options for the model
    class Meta:
        # Set the name of the database table for this model to "users"
        db_table = 'users' 
    # Define a string representation for the model, returning the useraccess field
    def __str__(self):
        return self.useraccess

