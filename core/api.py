# for FBV implementation
from urllib.error import HTTPError  # noqa: F401

from rest_framework import status  # noqa: F401
from rest_framework.decorators import api_view  # noqa: F401
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission

# for FBV implementation
from rest_framework.response import Response  # noqa: F401

from core.models import Ticket
from core.serializer import TicketLightSerializer, TicketSerializer


class HasPermission(BasePermission):

    """class for checking user authorization"""

    def has_permission(self, request, view):

        # NOTE: Refers to the first part of the task, where all tickets could be received by anyone.
        # method_list = ["POST", "PUT", "DELETE"]
        # if request.method in method_list:
        #     return request.user.is_authenticated
        # return True

        method_list = ["POST", "PUT", "DELETE", "GET"]
        if request.method in method_list:
            return request.user.is_authenticated
        return False


# NOTE: added a "description" field to TicketLightSerializer and included it with "extra_kwargs".
# I am not sure if this is the correct approach, because the LightSerializer is made so as not to load too much.
class TicketsListCreateAPI(ListCreateAPIView):
    http_method_names = ["post", "get"]
    serializer_class = TicketSerializer
    permission_classes = [HasPermission]
    queryset = Ticket.objects.all()

    def get_queryset(self):
        if self.request.method == "GET":
            # if the user is not admin
            if self.request.user.role_id == 2:
                self.serializer_class = TicketLightSerializer
                return Ticket.objects.filter(client=self.request.user)
            return Ticket.objects.all()


class TicketRetriveAPI(RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [HasPermission]
    lookup_field = "id"
    lookup_url_kwargs = "id"


# NOTE: FBV implementation. I keep it for myself as notes

# @api_view(["GET", "POST"])
# def get_post_tickets(request) -> dict:
#     if request.method == "GET":
#         tickets = Ticket.objects.all()
#         data = TicketLightSerializer(tickets, many=True).data
#         return Response(data=data)

#     try:
#         if request.user.is_authenticated:
#             serializer = TicketSerializer(data=request.data)
#             serializer.is_valid()
#             instance = serializer.create(serializer.validated_data)
#             results = TicketSerializer(instance).data
#             return Response(data=results, status=status.HTTP_201_CREATED)
#     except HTTPError:
#         data = {"details": "User has no authentetication token or token is invalid"}
#         return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(["GET", "PUT", "DELETE"])
# def retrieve_update_delete_ticket(request, id_: int) -> dict:
#     initial_ticket = Ticket.objects.get(id=id_)

#     try:
#         if request.method == "GET":
#             data = TicketSerializer(initial_ticket).data
#             return Response(data=data)

#         elif request.method == "PUT" and request.user.is_authenticated:
#             serializer = TicketSerializer(data=request.data, partial=True)
#             serializer.is_valid()
#             instance = serializer.update(initial_ticket, serializer.validated_data)
#             results = TicketSerializer(instance).data
#             return Response(data=results)

#         elif request.method == "DELETE" and request.user.is_authenticated:
#             initial_ticket.delete()
#             return Response({"message": "Ticket was deleted"}, status=status.HTTP_204_NO_CONTENT)
#     except HTTPError:
#         data = {"details": "User has no authentetication token or token is invalid"}
#         return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
