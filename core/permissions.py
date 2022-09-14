from django.core.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from authentication.models import DEFAULT_ROLES


class OperatorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.id == DEFAULT_ROLES["admin"]:
            return True
        return False


class HasPermission(BasePermission):

    """class for checking user authorization"""

    def has_permission(self, request, view):

        # NOTE: Refers to the first part of the task, where all tickets could be received by anyone.
        # method_list = ["POST", "PUT", "DELETE"]
        # if request.method in method_list:
        #     return request.user.is_authenticated
        # return True

        method_list = ["POST", "PUT", "DELETE", "GET"]

        # NOTE: If admin is trying to create a ticket, application raises an error
        if request.method == "POST" and request.user.role.id == DEFAULT_ROLES["admin"]:
            raise ValidationError("Only the user (not admin) can create a ticket")

        # NOTE: If name of "empty" parameter is incorrect
        if request.method == "GET" and request.GET.get("empty") not in [None, "true", "false"]:
            raise ValidationError("ErrorName. Parameter 'empty' can be 'true' or 'false'")

        if request.method in method_list:
            return request.user.is_authenticated
        return False
