from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings

class IsAdminOrEmployee(BasePermission):
    def has_permission(self, request, view):
        jwt_token = request.headers.get('Authorization')
        if jwt_token:
            jwt_token = jwt_token.split(' ')[1]
            # Get the user data from the JWT token payload
            payload = jwt.decode(jwt_token.encode(), settings.SECRET_KEY, algorithms=['HS256'])
            user_data = payload.get('user_data')
            user_type = user_data.get('UserType')
            if user_type == 'Administrator':
                # Allow access to all API endpoints for Administrator
                return True
            elif user_type == 'Employees':
                # Allow access to specific API endpoints for Employee
                if request.method in ['GET', 'PUT', 'PATCH']:
                    return True
                return False
        return False

