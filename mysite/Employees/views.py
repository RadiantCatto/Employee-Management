from django.core.paginator import Paginator
from django.db.models import CharField, F, Q, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employees, WorkSchedules
from .serializers import EmployeesSerializer, WorkSchedulesSerializer
#Class EmployeeDetails Specific ID include workschedule records
class EmployeeDetails(APIView):
    # A helper method to get an employee object by primary key
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            # If employee with given pk does not exist, raise Http404 exception
            raise Http404

    # Handle GET request for a specific employee with the given pk
    def get(self, request, pk):
        # Get the employee object with given pk
        employee = self.get_object(pk)

        # Serialize the employee object using EmployeesSerializer
        serializer = EmployeesSerializer(employee)
        employee_data = serializer.data

        # Get all workschedules related to the employee object
        workschedules = employee.workschedule_set.all()

        # Serialize the workschedules using WorkScheduleSerializer
        workschedule_serializer = WorkSchedulesSerializer(workschedules, many=True)
        workschedule_data = workschedule_serializer.data

        # Add the serialized workschedules to employee data dictionary
        employee_data['WorkSchedules'] = workschedule_data

        # Return the serialized employee data as a JSON response
        return Response(employee_data)
    
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

# class WorkSchedulesView List Employees's WorkSchedules Define a view to handle creating work schedules
class WorkSchedulesView(APIView):

    def get(self, request, format=None):
        work_schedules = WorkSchedules.objects.all()
        serializer = WorkSchedulesSerializer(work_schedules, many=True)
        return Response(serializer.data)
    def post(self, request):
        try:
            # Get the data from the request
            workschedules_data = request.data
            # Get a list of employee IDs from the workschedule data
            employee_id_list = [int(workschedule['employee']) for workschedule in workschedules_data]
            # Delete any existing workschedules for the specified employees
            existing_workschedules = WorkSchedules.objects.filter(employee_id__in=employee_id_list)
            existing_workschedules.delete()

            # Create a serializer for the workschedule data
            workschedules_serializer = WorkSchedulesSerializer(data=workschedules_data, many=True)

            # If the serializer is valid, save the data and return a success response
            if workschedules_serializer.is_valid():
                workschedules_serializer.save()
                return Response(workschedules_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If the serializer is not valid, return an error response
                return Response(workschedules_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # If an error occurs, return a server error response
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
