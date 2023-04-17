from rest_framework import serializers
from .models import Users


# Define a serializer for the Users model, inheriting from Django REST Framework's ModelSerializer class
class UsersSerializer(serializers.ModelSerializer):
    # Define a Meta class to provide additional options for the serializer
    class Meta:
        # Set the model for the serializer to the Users model
        model = Users
        # Specify that all fields in the model should be included in the serialized output
        fields = '__all__'