from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Users
from .serializers import UsersSerializer

class CreateUserView(APIView):
    serializer_class = UsersSerializer

    def post(self, request, format=None):
        employee_id = request.data.get('employee_id')
        useraccess = request.data.get('useraccess')
        passphrase = request.data.get('passphrase')

        # Check if employee already has an account
        if Users.objects.filter(employee_id=employee_id).exists():
            return Response({'error': 'Employee already has an account'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if Users.objects.filter(useraccess=useraccess).exists():
            return Response({'error': 'Username already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password format
        if not is_valid_password(passphrase):
            return Response({'error': 'Invalid password format'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate salt and hash password
        salt = generate_salt()
        hashed_passphrase = make_password(passphrase, salt=salt)

        # Create user record
        data = {'employee_id': employee_id, 'useraccess': useraccess, 'passphrase': hashed_passphrase, 'salt': salt}
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_valid_password(password):
        # Implement password validation logic here
        return True

    def generate_salt():
        # Implement salt generation logic here
        return 'randomsalt'
