from django.contrib import admin

from apps.authentication.models import Role, User
from apps.core.models import Ticket


class TicketsForClient(admin.TabularInline):
    model = Ticket
    fk_name = "client"
    extra = 0


class TicketsForOperator(admin.TabularInline):
    model = Ticket
    fk_name = "operator"
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]
    readonly_fields = ["password", "last_login"]
    # filtering for Users by age
    list_filter = ["age"]
    inlines = [TicketsForClient, TicketsForOperator]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
