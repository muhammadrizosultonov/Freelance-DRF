from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "project",
            "client",
            "freelancer",
            "agreed_price",
            "status",
            "created_at",
            "finished_at",
        ]
        read_only_fields = fields
