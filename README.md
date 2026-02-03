# Personal CRM + Accounting (Django)

This is a single-user CRM designed for personal/internal use. It combines lightweight CRM features with basic accounting (invoices, payments, expenses) and HR management for employee leave and salary tracking.

## Features (MVP)

### CRM
- Contacts and companies
- Leads and opportunities
- Activities and notes

### Accounting
- Invoices with line items
- Payments tracking
- Expenses
- Basic chart of accounts

### HR
- Employee records
- Leave requests
- Payroll entries

## Files to check the website

The minimal website is served from the Django project and uses the default templates directory:

- `manage.py` to run the server
- `crm_project/settings.py` and `crm_project/urls.py` for configuration and routing
- `crm/urls.py` and `crm/views.py` for the home page
- `templates/home.html` for the landing page UI

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000/` for the landing page
- `http://127.0.0.1:8000/admin/` for admin

## Admin

All models are registered in the Django admin for quick management.
