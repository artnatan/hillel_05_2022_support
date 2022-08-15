from django.contrib import admin

from .models import Comment, Ticket


class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "theme",
        "operator",
        "client",
    ]
    list_display_links = ["theme"]
    # filtering for Tickets by operator
    list_filter = ["operator"]
    search_fields = ["theme"]
    inlines = [CommentsInLine]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "ticket"]
