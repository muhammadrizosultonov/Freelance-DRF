from django.urls import path
from .views import ReviewCreateView

urlpatterns = [
    path("contracts/<int:contract_id>/review/", ReviewCreateView.as_view(), name="contract-review"),
]
