from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Project
from .serializers import ProjectSerializer
from users.permissions import ClientOnly


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title"]
    filterset_fields = {"budget": ["gte", "lte"]}

    def get_queryset(self):
        return Project.objects.filter(status=Project.Status.OPEN).select_related("client")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), ClientOnly()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all().select_related("client")
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
