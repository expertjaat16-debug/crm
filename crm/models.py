from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("lost", "Lost"),
    ]

    name = models.CharField(max_length=255)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Opportunity(models.Model):
    STAGE_CHOICES = [
        ("prospecting", "Prospecting"),
        ("proposal", "Proposal"),
        ("negotiation", "Negotiation"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="prospecting")
    expected_close_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    TYPE_CHOICES = [
        ("call", "Call"),
        ("email", "Email"),
        ("meeting", "Meeting"),
        ("task", "Task"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("done", "Done"),
    ]

    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="open")
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.activity_type} ({self.status})"
