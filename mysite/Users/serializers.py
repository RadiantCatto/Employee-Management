
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
        # Get the employee ID from the validated data
        employee_id = validated_data.pop('employee_id')
        # Create a new User instance with the employee ID and validated data
        user = Users(employee_id=employee_id, **validated_data)
        # Save the User instance
        user.save()
        # Return the User instance
        return user

    def validate_employee_id(self, value):
        # Check if employee_id already exists in users table
        if Users.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee already has an account")
        return value
    
    def to_internal_value(self, data):
        # Try to get the internal value of the data using the base class implementation
        try:
            return super().to_internal_value(data)
        # Catch any validation errors raised by the base class implementation
        except serializers.ValidationError as exc:
            # Check if the error message contains the string "Invalid pk"
            if 'Invalid pk' in str(exc):
                # If it does, raise a new validation error with a custom error message for the employee_id field
                raise serializers.ValidationError({'employee_id': ['employee_id not exist please apply Employee']})
            # If the error message does not contain "Invalid pk", re-raise the original validation error
            raise exc
    
    def validate_useraccess(self, value):
        # Check if useraccess value is unique
        if Users.objects.filter(useraccess=value).exists():
            raise serializers.ValidationError("Username already in use")
        return value

    def validate_passphrase(self, value):
        # Perform custom password validation using Django's built-in password validation and third-party library django-password-validators
        validate_password(value)  # check length, common sequences, and other built-in validation rules
        return value