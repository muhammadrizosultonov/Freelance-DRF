from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from users.models import CustomUser


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(user1=user) | Q(user2=user))

    def create(self, request, *args, **kwargs):
        other_user_id = request.data.get("other_user_id")
        if not other_user_id:
            raise ValidationError("other_user_id majburiy.")
        other_user = CustomUser.objects.filter(id=other_user_id).first()
        if not other_user or other_user == request.user:
            raise ValidationError("Foydalanuvchi topilmadi.")
        conv = Conversation.get_or_create_between(request.user, other_user)
        serializer = self.get_serializer(conv)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(Q(conversation__user1=user) | Q(conversation__user2=user))
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset.order_by("created_at")

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if not conversation:
            raise ValidationError("conversation majburiy.")
        if self.request.user not in (conversation.user1, conversation.user2):
            raise PermissionDenied("Bu suhbat sizga tegishli emas.")
        serializer.save(sender=self.request.user)
