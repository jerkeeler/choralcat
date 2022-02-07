from django.contrib import admin

from .models import (
    Category,
    Composition,
    Instrument,
    Person,
    Program,
    Tag,
    Topic,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "timezone")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "user",
        "slug",
        "created_at",
        "updated_at",
    )
    search_fields = ("last_name", "first_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user", "created_at", "updated_at")
    search_fields = ["value"]


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "slug", "created_at", "updated_at")
    search_fields = ("token", "title")
    list_filter = ["user"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "season", "user", "slug", "created_at", "updated_at")
    search_fields = ("token", "title")
