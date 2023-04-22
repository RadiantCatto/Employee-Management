#class UsersListView modules ------
import uuid
import hashlib
#class UserLoginAPIView modules ------
import datetime
from datetime import timedelta

import jwt
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsersSerializer,EmployeesSerializer
from .models import Users

class UsersListView(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)   
     
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid():
            # Generate a unique salt for each record
            salt = uuid.uuid4().hex

            # Hash the plain text password with the generated salt
            password = serializer.validated_data['passphrase']
            # Encode the salted password as UTF-8 and hash it using SHA-512
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
            # Save the new user record to the database
            user = serializer.save(salt=salt, passphrase=hashed_password)
            # Return a response with the created user's employee_id, useraccess, and employee_id
            return Response({'UserType': user.UserType,
                             'employee_id': user.employee_id.id,
                             'employee_name': user.employee_id.firstname, 
                             'salt': user.salt,
                             'useraccess': user.useraccess,
                             'passphrase': user.passphrase,
                             'created_by': user.created_by
                             }, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            if 'non_field_errors' in errors:
                del errors['non_field_errors']
            # Return a response with the serializer's validation errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        # Get username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')     
        # Find user with given username
        try:
            user = Users.objects.get(useraccess=username)
        except Users.DoesNotExist:
            return Response({'error': 'Username does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user is active
        if not user.isActive:
            return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        
        # Verify password
        salt = user.salt
        hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

        if hashed_password != user.passphrase:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Serialize user and employee data
        user_serializer = UsersSerializer(user)
        employee_serializer = EmployeesSerializer(user.employee_id)
        serialized_user = user_serializer.data
        serialized_employee = employee_serializer.data
        
        # Remove passphrase and salt from serialized user data
        serialized_user.pop('passphrase', None)
        serialized_user.pop('salt', None)
        
        # Combine user and employee data into a single dictionary
        user_data = {**serialized_user, **serialized_employee}
        
        # Generate JWT token with expiration time of 1 hour
        jwt_payload = {
            'user_data': user_data,
            'exp': datetime.datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm='HS256')
        
        # Return serialized user and JWT token in response
        return Response({'user': user_data, 'jwt_token': jwt_token})