from django.contrib import admin

from .models import Activity, Company, Contact, Lead, Opportunity


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "phone")
    search_fields = ("name", "website")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "company")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("company",)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "source")
    list_filter = ("status",)
    search_fields = ("name", "source")


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "value", "stage", "expected_close_date")
    list_filter = ("stage",)
    search_fields = ("name",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("activity_type", "status", "due_date", "contact", "company")
    list_filter = ("activity_type", "status")
    search_fields = ("notes",)
