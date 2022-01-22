from django.contrib import admin

from .models import Person, Category, Instrument, Tag, Composition, Program


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "user", "name_slug")
    search_fields = ("last_name", "first_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user")
    search_fields = ["value"]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user")
    search_fields = ["value"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "user")
    search_fields = ["value"]


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "title_slug")
    search_fields = ("token", "title")
    list_filter = ["user"]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "season", "user", "title_slug")
    search_fields = ("token", "title")
