from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, BidViewSet, ContractViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"bids", BidViewSet, basename="bid")
router.register(r"contracts", ContractViewSet, basename="contract")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls
