from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "project",
        "client",
        "freelancer",
        "agreed_price",
        "status",
        "created_at",
    ]
    list_filter = ["status"]
    search_fields = ["project__title", "client__username", "freelancer__username"]
