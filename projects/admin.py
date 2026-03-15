from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "client", "budget", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "client__username"]
