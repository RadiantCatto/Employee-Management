from django.db import models

# Create your models here.

class Employees(models.Model):
    firstname = models.CharField('First Name: ',max_length=255, null=True)
    middlename = models.CharField('Middle Name: ',max_length=255, null=True)
    lastname = models.CharField('Last Name: ',max_length=255, null=True)
    suffix = models.CharField('Suffix: ',max_length=255, null=True)
    birthday = models.DateField('Birthday' , auto_now=False, auto_now_add=False, null=True)
    gender = models.CharField('Gender: ',max_length=255, null=True)
    civilstatus = models.CharField('Civil Status: ',max_length=255, null=True)
    created_date = models.DateTimeField('Created Date: ',auto_now_add=True, null=True)
    updated_date = models.DateTimeField('Updated Data: ',auto_now=True, null=True)
    isRegular = models.BooleanField(default=False)  # new column
    RegularizationDate = models.DateField(null=True)  # new column
    EmploymentDate = models.DateField(null=True)  # new column
    class Meta:
        db_table = 'Employees'
        

