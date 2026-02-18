from django.contrib import admin

from .models import (
    Account,
    Expense,
    Invoice,
    InvoiceLine,
    LedgerAccount,
    LedgerEntry,
    Party,
    Payment,
    Product,
    ProductCategory,
    PurchaseBill,
    PurchaseLine,
)


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "party_type", "mobile_number", "opening_balance", "credit_limit")
    list_filter = ("party_type", "is_active")
    search_fields = ("name", "mobile_number", "gst_number")


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "purchase_price",
        "selling_price",
        "current_stock",
        "low_stock_alert",
    )
    list_filter = ("category",)
    search_fields = ("name", "sku")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "party", "issue_date", "due_date", "status")
    list_filter = ("status",)
    search_fields = ("number", "party__name")
    inlines = [InvoiceLineInline, PaymentInline]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "category", "amount", "vendor", "payment_mode")
    search_fields = ("category", "vendor")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type")
    list_filter = ("account_type",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "paid_date", "method")
    list_filter = ("method",)


class PurchaseLineInline(admin.TabularInline):
    model = PurchaseLine
    extra = 1


@admin.register(PurchaseBill)
class PurchaseBillAdmin(admin.ModelAdmin):
    list_display = ("number", "supplier", "bill_date", "status")
    list_filter = ("status",)
    search_fields = ("number", "supplier__name")
    inlines = [PurchaseLineInline]


@admin.register(LedgerAccount)
class LedgerAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "opening_balance")
    list_filter = ("account_type",)
    search_fields = ("name",)


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_date", "party", "account", "entry_type", "amount")
    list_filter = ("entry_type", "account")
    search_fields = ("reference", "party__name")
