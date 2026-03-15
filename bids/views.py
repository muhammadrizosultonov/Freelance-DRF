from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Bid
from .serializers import BidSerializer
from projects.models import Project
from contracts.models import Contract
from users.permissions import ClientOnly, FreelancerOnly, IsProjectOwner


class ProjectBidCreateView(APIView):
    permission_classes = [IsAuthenticated, FreelancerOnly]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if project.status != Project.Status.OPEN:
            return Response({"detail": "Project is not open."}, status=status.HTTP_400_BAD_REQUEST)

        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            return Response({"detail": "You already bid on this project."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, freelancer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectBidListView(ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs["project_id"])
        self.check_object_permissions(self.request, project)
        return project.bids.all().select_related("freelancer", "project")


class BidAcceptView(APIView):
    permission_classes = [IsAuthenticated, ClientOnly]

    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project

        if project.client != request.user:
            return Response(
                {"detail": "Only the project owner can accept bids."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if project.status != Project.Status.OPEN:
            return Response({"detail": "Project is not open."}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(project, "contract"):
            return Response(
                {"detail": "Contract already exists for this project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Bid.objects.filter(project=project).exclude(id=bid.id).update(status=Bid.Status.REJECTED)
        bid.status = Bid.Status.ACCEPTED
        bid.save(update_fields=["status"])

        project.status = Project.Status.IN_PROGRESS
        project.save(update_fields=["status"])

        Contract.objects.create(
            project=project,
            client=project.client,
            freelancer=bid.freelancer,
            agreed_price=bid.price,
        )

        return Response({"detail": "Bid accepted and contract created."}, status=status.HTTP_200_OK)
