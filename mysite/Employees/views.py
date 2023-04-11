from django.core.paginator import Paginator
from django.db.models import CharField, F, Q, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employees
from .serializers import EmployeesSerializer

class EmployeeDetails(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404

    def get(self, request, pk):  # add pk parameter here
        employees = self.get_object(pk)
        serializer = EmployeesSerializer(employees)
        return Response(serializer.data)
    
class MainEmployees(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404

    def get(self, request):
        keyword = request.GET.get('keyword', '')
        employees = Employees.objects.filter(
            Q(firstname__icontains=keyword) |
            Q(middlename__icontains=keyword) |
            Q(lastname__icontains=keyword) 
            )
        # apply pagination
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(employees, page_size)
        page_number = request.GET.get('page_number', 1)
        employees_page = paginator.get_page(page_number)
        serializer = EmployeesSerializer(employees_page, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeesSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeesRegularization(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            return Response({'error': 'employee record does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        employee = self.get_object(pk)
        is_regular = request.data.get('isRegular')
        regularization_date = request.data.get('RegularizationDate')

        # Check if both columns are supplied
        if is_regular is None or regularization_date is None:
            return Response({'error': 'Both isRegular and RegularizationDate must be supplied.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the employee is already set as regular
        if employee.isRegular and employee.RegularizationDate is not None:
            return Response({'error': 'Employee is already set as regular.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the employee record
        serializer = EmployeesSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
