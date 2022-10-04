from django.db.models import Q
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response

from apps.authentication.models import DEFAULT_ROLES
from apps.core.models import Ticket
from apps.core.permissions import OperatorOnly, UserPermissions
from apps.core.serializers.tickets import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
)
from apps.core.services import TicketCRUD


class TicketsListCreateAPI(ListCreateAPIView):
    http_method_names = ["post", "get"]
    permission_classes = [UserPermissions]
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if self.request.method == "GET" and user.role_id == DEFAULT_ROLES["user"]:
            return TicketLightSerializer
        return TicketSerializer

    def get_queryset(self):
        user = self.request.user
        # check that parametr "empty" is enabled
        if "empty" in self.request.query_params.keys():
            filter_parameter = self.request.query_params["empty"]
        filter_parameter = ""

        if self.request.method == "GET":
            # if the user is not admin
            if user.role_id == DEFAULT_ROLES["user"]:
                return Ticket.objects.filter(client=user)

            # NOTE: returns tickets with "empty" parametr
            # error output is described in permission.py
            elif user.role_id == DEFAULT_ROLES["admin"] and filter_parameter != "":
                if filter_parameter == "true":
                    return Ticket.objects.filter(operator__isnull=True)
                else:
                    return Ticket.objects.filter(operator=user)

            # NOTE: returns all tickets with no operator and ticket where this admin is operator
            return Ticket.objects.filter(Q(operator__isnull=True) | Q(operator=user))


class TicketRetriveAPI(RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [UserPermissions]
    lookup_field = "id"
    lookup_url_kwargs = "id"

    def get_queryset(self):
        user = self.request.user
        if user.role_id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


class TicketAssignAPI(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = TicketAssignSerializer
    permission_classes = [OperatorOnly]
    lookup_field = "id"
    lookup_url_kwargs = "id"

    def get_queryset(self):
        return Ticket.objects.filter(operator=None)


class TicketResolveAPI(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = TicketLightSerializer
    permission_classes = [OperatorOnly]
    lookup_field = "id"
    lookup_url_kwargs = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(operator=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = TicketCRUD.change_resolved_status(instance)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


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
