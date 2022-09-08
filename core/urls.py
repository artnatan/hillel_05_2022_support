from django.urls import path

from core.api import TicketRetriveAPI, TicketsListCreateAPI

urlpatterns = [
    path("", TicketsListCreateAPI.as_view()),
    path("<int:id>/", TicketRetriveAPI.as_view()),
]
