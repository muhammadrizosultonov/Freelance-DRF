from django.urls import path
from .views import ProjectBidCreateView, ProjectBidListView, BidAcceptView

urlpatterns = [
    path("projects/<int:project_id>/bid/", ProjectBidCreateView.as_view(), name="project-bid-create"),
    path("projects/<int:project_id>/bids/", ProjectBidListView.as_view(), name="project-bid-list"),
    path("bids/<int:bid_id>/accept/", BidAcceptView.as_view(), name="bid-accept"),
]
