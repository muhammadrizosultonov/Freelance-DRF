from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Project, Bid, Contract, Review
from .serializers import ProjectSerializer, BidSerializer, ContractSerializer, ReviewSerializer
from users.models import CustomUser


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Role.CLIENT:
            return Project.objects.filter(client=user).order_by("-created_at")
        return Project.objects.filter(status=Project.StatusChoices.OPEN).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != CustomUser.Role.CLIENT:
            raise PermissionDenied("Faqat mijoz loyiha yarata oladi.")
        serializer.save(client=user, status=Project.StatusChoices.OPEN)

    def perform_update(self, serializer):
        if serializer.instance.client != self.request.user:
            raise PermissionDenied("Faqat o'z loyihangizni tahrirlashingiz mumkin.")
        serializer.save()


class BidViewSet(viewsets.ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Role.FREELANCER:
            return Bid.objects.filter(freelancer=user).order_by("-created_at")
        return Bid.objects.filter(project__client=user).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != CustomUser.Role.FREELANCER:
            raise PermissionDenied("Faqat freelancer ariza yubora oladi.")
        project = serializer.validated_data.get("project")
        if project.status != Project.StatusChoices.OPEN:
            raise ValidationError("Loyiha arizaga yopiq.")
        serializer.save(freelancer=user, status=Bid.StatusChoices.PENDING)


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Role.CLIENT:
            return Contract.objects.filter(client=user).order_by("-created_at")
        return Contract.objects.filter(freelancer=user).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != CustomUser.Role.CLIENT:
            raise PermissionDenied("Faqat mijoz shartnoma yarata oladi.")
        project = serializer.validated_data.get("project")
        if project.client != user:
            raise PermissionDenied("Bu loyiha sizga tegishli emas.")
        serializer.save(client=user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Role.CLIENT:
            return Review.objects.filter(client=user).order_by("-created_at")
        return Review.objects.filter(freelancer=user).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != CustomUser.Role.CLIENT:
            raise PermissionDenied("Faqat mijoz baho bera oladi.")
        contract = serializer.validated_data.get("contract")
        if contract.client != user:
            raise PermissionDenied("Bu shartnoma sizga tegishli emas.")
        if contract.status not in [Contract.StatusChoices.FINISHED, Contract.StatusChoices.CANCELLED]:
            raise ValidationError("Faqat tugallangan yoki bekor qilingan shartnomalarda baho beriladi.")
        serializer.save(client=user, freelancer=contract.freelancer)
