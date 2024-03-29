from apps.core.models import Ticket


class TicketCRUD:
    @staticmethod
    def change_resolved_status(instance: Ticket) -> Ticket:

        """Change Ticket object's resolved status to the opposite"""
        instance.resolved = not instance.resolved
        instance.save()

        return instance
