from rest_framework.generics import CreateAPIView, ListAPIView

from apps.core.models import Comment, Ticket
from apps.core.serializers import CommentSerializer


class CommentsListAPI(ListAPIView):
    http_method_names = ["get"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwargs = "ticket_id"

    def get_queryset(self):
        ticket_id = self.kwargs[self.lookup_field]
        ticket: Ticket = Ticket.objects.get(id=ticket_id)

        # only the user of the ticket can see the comments
        if ticket.operator == self.request.user or ticket.client == self.request.user:
            return Comment.objects.filter(ticket_id=ticket_id)
        raise ValueError("You are not a ticket operator or a ticket client")


class CommentsCreateAPI(CreateAPIView):
    http_method_names = ["post"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwargs = "ticket_id"

    def get_queryset(self):
        ticket_id = self.kwargs[self.lookup_field]

        return Comment.objects.filter(ticket_id=ticket_id)
