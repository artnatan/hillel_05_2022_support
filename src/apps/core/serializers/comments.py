from rest_framework import serializers

from apps.core.models import Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict) -> dict:

        request = self.context["request"]

        ticket_id: id = request.parser_context["kwargs"]["ticket_id"]
        ticket: Ticket = Ticket.objects.get(id=ticket_id)

        # check for ticket operator and ticket resolved
        if not ticket.operator:
            raise ValueError("Unable to comment. Ticket operator must be appointed first.")
        elif ticket.resolved:
            raise ValueError("Unable to comment. Ticket resolved.")

        attrs["ticket"] = ticket
        attrs["user"] = request.user

        last_comment = ticket.comments.last()

        attrs["prev_comment"] = last_comment if last_comment else None

        return attrs
