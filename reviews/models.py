from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from contracts.models import Contract


class Review(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review #{self.id} - {self.contract.id}"
