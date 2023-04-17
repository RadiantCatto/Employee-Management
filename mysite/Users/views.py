from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Users
from .serializers import UsersSerializer

# Define a class-based view to create a new user
class CreateUserView(APIView):

    # Define the serializer class to use
    serializer_class = UsersSerializer

    # Define the POST method to handle creating a new user
    def post(self, request, format=None):

        # Retrieve the necessary data from the request
        employee_id = request.data.get('employee_id')
        useraccess = request.data.get('useraccess')
        passphrase = request.data.get('passphrase')

        # Check if the employee already has an account
        if Users.objects.filter(employee_id=employee_id).exists():
            return Response({'error': 'Employee already has an account'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists
        if Users.objects.filter(useraccess=useraccess).exists():
            return Response({'error': 'Username already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password format using a separate method
        if not is_valid_password(passphrase):
            return Response({'error': 'Invalid password format'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a salt and hash the password
        salt = generate_salt()
        hashed_passphrase = make_password(passphrase, salt=salt)

        # Create a new user record
        data = {'employee_id': employee_id, 'useraccess': useraccess, 'passphrase': hashed_passphrase, 'salt': salt}
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Define a method to validate the password format
    def is_valid_password(password):
        # Implement password validation logic here
        return True

    # Define a method to generate a random salt
    def generate_salt():
        # Implement salt generation logic here
        return 'randomsalt'