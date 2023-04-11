
from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Employees

class EmployeesSerializer(serializers.ModelSerializer):
    tenureship = serializers.SerializerMethodField()

    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'middle_name', 'last_name',
                  'full_name', 'suffix', 'birthday', 'civil_status',
                  'create_date', 'update_date', 'salary', 'hire_date', 
                  'isRegular', 'RegularizationDate', 'EmploymentDate', 'tenureship')

    def get_tenureship(self, obj):
        today = datetime.now().date()
        employment_date_str = str(obj.EmploymentDate)
        employment_date = datetime.strptime(employment_date_str, '%Y-%m-%d').date()
        years_of_service = (today - employment_date) // timedelta(days=365)

        # Set the "tenureship" field value based on the employment duration
        if years_of_service < 5:
            return 'short-tenure'
        else:
            return 'long-tenure'


    def validate_birthday(self, value):
        """
        Validate that the birthdate is a valid date and not a future date
        """
        today = datetime.today().date()
        try:
            if not value:
                raise serializers.ValidationError("birthdate field is required")
            elif value > today:
                raise serializers.ValidationError("birthdate cannot be a future date")
            else:
                return value
        except (TypeError, ValueError):
            raise serializers.ValidationError("invalid date format for birthdate")

    def to_internal_value(self, data):
        """
        Remove middle_name and suffix fields if they are not present in request data
        """
        if 'middle_name' not in data:
            data['middle_name'] = None
        if 'suffix' not in data:
            data['suffix'] = None
        return super().to_internal_value(data)