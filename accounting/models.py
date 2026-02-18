from django.db import models


class Party(models.Model):
    TYPE_CHOICES = [
        ("customer", "Customer"),
        ("supplier", "Supplier"),
        ("both", "Both"),
    ]

    party_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="customer")
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    gst_number = models.CharField(max_length=50, blank=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    advance_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    low_stock_alert = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sku = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:
        return self.name


class Account(models.Model):
    TYPE_CHOICES = [
        ("asset", "Asset"),
        ("liability", "Liability"),
        ("equity", "Equity"),
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self) -> str:
        return f"{self.name} ({self.account_type})"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
        ("draft", "Draft"),
    ]

    number = models.CharField(max_length=50, unique=True)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="invoices")
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Invoice {self.number}"

    @property
    def subtotal(self) -> float:
        return sum(line.line_total for line in self.lines.all())

    @property
    def gst_amount(self) -> float:
        return sum(line.gst_amount for line in self.lines.all())

    @property
    def total(self) -> float:
        return float(self.subtotal) + float(self.gst_amount) - float(self.discount_amount)

    @property
    def total_paid(self) -> float:
        return sum(float(payment.amount) for payment in self.payments.all())

    @property
    def balance_due(self) -> float:
        return float(self.total) - float(self.total_paid)


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def line_total(self) -> float:
        return float(self.quantity) * float(self.unit_price)

    @property
    def gst_amount(self) -> float:
        return float(self.line_total) * (float(self.gst_percent) / 100)


class Payment(models.Model):
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("upi", "UPI"),
        ("other", "Other"),
    ]

    invoice = models.ForeignKey(Invoice, related_name="payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField()
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)


class PurchaseBill(models.Model):
    STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
        ("draft", "Draft"),
    ]

    number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        Party, on_delete=models.PROTECT, related_name="purchase_bills"
    )
    bill_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Purchase {self.number}"

    @property
    def total(self) -> float:
        return sum(line.line_total for line in self.lines.all())


class PurchaseLine(models.Model):
    purchase_bill = models.ForeignKey(
        PurchaseBill, related_name="lines", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def line_total(self) -> float:
        return float(self.quantity) * float(self.unit_price)


class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=Payment.METHOD_CHOICES, default="cash")
    vendor = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.category} - {self.amount}"


class LedgerAccount(models.Model):
    TYPE_CHOICES = [
        ("cash", "Cash"),
        ("bank", "Bank"),
    ]

    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.name} ({self.account_type})"


class LedgerEntry(models.Model):
    ENTRY_CHOICES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]

    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    account = models.ForeignKey(
        LedgerAccount, on_delete=models.SET_NULL, null=True, blank=True
    )
    entry_date = models.DateField()
    entry_type = models.CharField(max_length=10, choices=ENTRY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0)
