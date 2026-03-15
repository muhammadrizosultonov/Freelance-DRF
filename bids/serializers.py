from rest_framework import serializers
from .models import Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "project",
            "freelancer",
            "price",
            "message",
            "created_at",
            "status",
        ]
        read_only_fields = ["id", "project", "freelancer", "created_at", "status"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
