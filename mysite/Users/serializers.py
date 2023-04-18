
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Users, Employees


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ( 'firstname', 'middlename', 'lastname',
                   'suffix', 'birthday', 'civilstatus',
                  'created_date', 'updated_date',  'isRegular',
                  'RegularizationDate', 'EmploymentDate')

class UsersSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employees.objects.all())

    class Meta:
        model = Users
        fields = ('id', 'employee_id', 'useraccess', 'passphrase', 'created_by')

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        user = Users.objects.create(employee_id=employee_id, **validated_data)
        return user

    def validate_employee_id(self, value):
        # Check if employee_id already exists in users table
        if Users.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee already has an account")
        return value
    
    def validate_useraccess(self, value):
        # Check if useraccess value is unique
        if Users.objects.filter(useraccess=value).exists():
            raise serializers.ValidationError("Username already in use")
        return value

    def validate_passphrase(self, value):
        # Perform custom password validation using Django's built-in password validation and third-party library django-password-validators
        validate_password(value)  # check length, common sequences, and other built-in validation rules
        return value