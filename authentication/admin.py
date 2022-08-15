from django.contrib import admin

from core.models import Ticket

from .models import Role, User


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
