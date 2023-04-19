import uuid
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsersSerializer
from .models import Users

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            if 'non_field_errors' in errors:
                del errors['non_field_errors']
            # Return a response with the serializer's validation errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class UsersListView(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

