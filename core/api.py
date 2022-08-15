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
    serializer = TicketSerializer(data=request.data)
    serializer.is_valid()
    instance = serializer.create(serializer.validated_data)
    results = TicketSerializer(instance).data
    return Response(data=results, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def retrieve_update_delete_ticket(request, id_: int) -> dict:
    initial_ticket = Ticket.objects.get(id=id_)
    if request.method == "GET":
        data = TicketSerializer(initial_ticket).data
        return Response(data=data)
    elif request.method == "PUT":
        serializer = TicketSerializer(data=request.data, partial=True)
        serializer.is_valid()
        instance = serializer.update(initial_ticket, serializer.validated_data)
        results = TicketSerializer(instance).data
        return Response(data=results)

    # NOTE: I made the PUT method in the same way as we did the POST method in the lesson.
    # Code above.
    # Basically, in the examples I met the code below (both when using the PUT method
    # and the POST method). This edition uses the save() method instead of update() if PUT,
    # and create() if POST. Also serialization happens only once. And checking for validity,
    # instead of leading to validity.

    # serializer = TicketSerializer(initial_ticket, data=request.data, partial=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(data=serializer.data)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        initial_ticket.delete()
        return Response({"message": "Ticket was deleted"}, status=status.HTTP_204_NO_CONTENT)
