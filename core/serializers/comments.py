from rest_framework import serializers

from core.models import Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user"]

    def validate(self, attrs: dict) -> dict:

        ticket_id = self.context["request"].parser_context["kwargs"]["ticket_id"]
        attrs["ticket"] = Ticket.objects.get(id=ticket_id)

        return attrs
