from django.urls import path
from .views import ContractListView, ContractFinishView

urlpatterns = [
    path("contracts/", ContractListView.as_view(), name="contract-list"),
    path("contracts/<int:contract_id>/finish/", ContractFinishView.as_view(), name="contract-finish"),
]
