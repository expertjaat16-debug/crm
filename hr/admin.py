from django.contrib import admin

from .models import Employee, LeaveRequest, PayrollEntry


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "job_title", "salary")
    search_fields = ("first_name", "last_name", "email")


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "leave_type", "start_date", "end_date", "status")
    list_filter = ("leave_type", "status")


@admin.register(PayrollEntry)
class PayrollEntryAdmin(admin.ModelAdmin):
    list_display = ("employee", "period_start", "period_end", "gross_pay", "net_pay", "paid_date")
    list_filter = ("paid_date",)
