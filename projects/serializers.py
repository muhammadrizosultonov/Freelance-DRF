from django.utils import timezone
from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "budget", "deadline", "status", "created_at", "client",]
        read_only_fields = ["id", "status", "created_at", "client"]

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget must be greater than 0.")
        return value

    def validate_deadline(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError("Deadline must be today or in the future.")
        return value
