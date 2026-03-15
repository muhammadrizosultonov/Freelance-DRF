from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

CustomUser = get_user_model()


class ClientOnly(BasePermission):
    message = "Only clients can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Role.CLIENT
        )


class FreelancerOnly(BasePermission):
    message = "Only freelancers can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Role.FREELANCER
        )


class IsProjectOwner(BasePermission):
    message = "You are not the owner of this project."

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.client == request.user)


class IsContractParticipant(BasePermission):
    message = "You are not a participant of this contract."

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and (obj.client == request.user or obj.freelancer == request.user)
        )
