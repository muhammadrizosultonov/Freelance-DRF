from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "contract", "rating", "created_at"]
    search_fields = ["contract__project__title", "contract__client__username"]
