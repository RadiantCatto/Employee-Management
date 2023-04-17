from django.db import models
from Employees.models import Employees
# Create your models here.
#Users model
class Users(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    useraccess = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    class Meta:
        # Set the name of the database table for this model
        db_table = 'users' 
    def __str__(self):
        return self.useraccess

