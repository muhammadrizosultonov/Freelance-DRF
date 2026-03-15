from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "budget",
            "deadline",
            "status",
            "created_at",
            "client",
        ]
        read_only_fields = ["id", "status", "created_at", "client"]
