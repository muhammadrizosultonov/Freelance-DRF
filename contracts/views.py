from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contract
from .serializers import ContractSerializer
from projects.models import Project
from users.permissions import ClientOnly, IsContractParticipant


class ContractListView(ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(Q(client=user) | Q(freelancer=user)).select_related(
            "project", "client", "freelancer"
        )


class ContractFinishView(APIView):
    permission_classes = [IsAuthenticated, ClientOnly, IsContractParticipant]

    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        self.check_object_permissions(request, contract)

        if contract.client != request.user:
            return Response(
                {"detail": "Only the client can finish the contract."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if contract.status != Contract.Status.ACTIVE:
            return Response({"detail": "Contract is not active."}, status=status.HTTP_400_BAD_REQUEST)

        contract.status = Contract.Status.FINISHED
        contract.finished_at = timezone.now()
        contract.save(update_fields=["status", "finished_at"])

        project = contract.project
        project.status = Project.Status.COMPLETED
        project.save(update_fields=["status"])

        return Response({"detail": "Contract finished."}, status=status.HTTP_200_OK)
