from django.core.exceptions import BadRequest, ValidationError
from rest_framework.permissions import BasePermission

from apps.authentication.models import DEFAULT_ROLES


class OperatorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.id == DEFAULT_ROLES["admin"]:
            return True
        return False


class UserPermissions(BasePermission):

    """class for checking user authorization"""

    def has_permission(self, request, view):
        method_list = ["POST", "PUT", "DELETE", "GET"]

        # NOTE: If admin is trying to create a ticket, application raises an error
        if request.method == "POST" and request.user.role.id == DEFAULT_ROLES["admin"]:
            raise ValidationError("Only the user (not admin) can create a ticket")

        # NOTE: If name of "empty" parameter is incorrect or value is incorrect
        if "empty" in request.query_params.keys():
            if request.method == "GET" and request.query_params["empty"] not in ["true", "false"]:
                raise BadRequest("ErrorName. Parameter 'empty' can be 'true' or 'false'")
        elif request.query_params:
            raise BadRequest("ErrorName. Parameter specified incorrectly")

        if request.method in method_list:
            return request.user.is_authenticated
        return False
