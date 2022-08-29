from urllib.error import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Ticket
from core.serializer import TicketLightSerializer, TicketSerializer


@api_view(["GET", "POST"])
def get_post_tickets(request) -> dict:
    if request.method == "GET":
        tickets = Ticket.objects.all()
        data = TicketLightSerializer(tickets, many=True).data
        return Response(data=data)

    try:
        if request.user.auth_token:
            serializer = TicketSerializer(data=request.data)
            serializer.is_valid()
            instance = serializer.create(serializer.validated_data)
            results = TicketSerializer(instance).data
            return Response(data=results, status=status.HTTP_201_CREATED)
    except HTTPError:
        data = {"details": "User has no authentetication token or token is invalid"}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "PUT", "DELETE"])
def retrieve_update_delete_ticket(request, id_: int) -> dict:
    initial_ticket = Ticket.objects.get(id=id_)

    try:
        if request.method == "GET":
            data = TicketSerializer(initial_ticket).data
            return Response(data=data)

        elif request.method == "PUT" and request.user.auth_token:
            serializer = TicketSerializer(data=request.data, partial=True)
            serializer.is_valid()
            instance = serializer.update(initial_ticket, serializer.validated_data)
            results = TicketSerializer(instance).data
            return Response(data=results)

        elif request.method == "DELETE" and request.user.auth_token:
            initial_ticket.delete()
            return Response({"message": "Ticket was deleted"}, status=status.HTTP_204_NO_CONTENT)
    except HTTPError:
        data = {"details": "User has no authentetication token or token is invalid"}
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
