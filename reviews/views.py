from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contracts.models import Contract
from users.permissions import ClientOnly, IsContractParticipant
from .serializers import ReviewSerializer


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        ref_name = "ReviewDetailResponse"


class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated, ClientOnly, IsContractParticipant]

    @swagger_auto_schema(
        operation_summary="Create review for finished contract",
        request_body=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: DetailSerializer,
            401: DetailSerializer,
            403: DetailSerializer,
            404: DetailSerializer,
        },
    )
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        self.check_object_permissions(request, contract)

        if contract.client != request.user:
            return Response(
                {"detail": "Only the client can leave a review."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if contract.status != Contract.Status.FINISHED:
            return Response(
                {"detail": "Contract must be finished before review."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if hasattr(contract, "review"):
            return Response(
                {"detail": "Review already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(contract=contract)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
