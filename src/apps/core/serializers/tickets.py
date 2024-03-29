from itertools import chain

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.authentication.models import Role
from apps.core.models import Ticket

User = get_user_model()


def user_as_dict(user: User) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
    }


def ticket_as_dict(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "theme": ticket.theme,
        "discription": ticket.description,
        "operator": user_as_dict(ticket.operator),
        "resolved": ticket.resolved,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
    }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "email",
            "username",
            "first_name",
            "last_name",
            "age",
            "phone",
        ]


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "operator",
            "client",
            "theme",
            "description",
            "resolved",
        ]

    def validate(self, attrs: dict) -> dict:
        theme = attrs.get("theme")

        if not theme:
            return attrs

        data = Ticket.objects.values_list("theme")
        # data = Ticket.objects.only("theme")
        for element in chain.from_iterable(data):
            if element == theme:
                raise ValidationError("This ticket is already in the database")

        attrs["client"] = self.context["request"].user

        return attrs


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "theme",
            "description",
            "resolved",
            "operator",
            "client",
        ]


class TicketAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["operator"]

    def validate(self, attrs):
        attrs["operator"] = self.context["request"].user
        return attrs
