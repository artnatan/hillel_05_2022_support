from django.http import JsonResponse


class TicketService:
    def get_all_tickets(self) -> dict:
        return {}


def get_all_tickets(request) -> dict:
    tickets_service = TicketService()
    data = tickets_service.get_all_tickets()

    return JsonResponse(data)
