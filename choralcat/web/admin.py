from django.contrib import admin

from .models import (
    Category,
    Composition,
    Instrument,
    Organization,
    Person,
    Program,
    Tag,
    Topic,
    UserProfile,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "token")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "timezone", "organization")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "organization",
        "slug",
        "created_at",
        "updated_at",
    )
    search_fields = ("last_name", "first_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "organization", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "organization", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "organization", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "organization", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "organization", "slug", "created_at", "updated_at")
    search_fields = ("token", "title")
    list_filter = ["organization"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "season", "organization", "slug", "created_at", "updated_at")
    search_fields = ("token", "title")
