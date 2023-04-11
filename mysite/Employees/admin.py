from django.contrib import admin
from .models import Employees as MyEmployees
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname","middlename", "suffix","birthday","gender","civilstatus","created_date","updated_date")

admin.site.register(MyEmployees, MemberAdmin)
