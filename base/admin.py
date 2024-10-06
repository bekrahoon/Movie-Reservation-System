from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from .models import Booking, Genre, Movie


@admin.register(Genre)
class GenreAdminClass(ModelAdmin):
    list_display = ["name"]
    search_feilds = "name"

    # Включаем Unfold функционал
    unfold_enabled = True

    # Сжатый режим полей в форме изменения
    compressed_fields = True

    # Предупреждение о несохранённых изменениях
    warn_unsaved_form = True

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Movie)
class MovieAdminClass(ModelAdmin):
    list_display = ["title", "description", "show_time"]
    search_fields = ["title", "description"]
    list_filter = ["genre", "show_time"]

    unfold_enabled = True
    compressed_fields = True
    warn_unsaved_form = True

    list_fullwidth = True  # Полный экран для списка
    list_filter_submit = True  # Кнопка для применения фильтров

    filter_horizontal = ("genre",)
    
    formfield_overrides = {
        ArrayField: {
            "widget": ArrayWidget,
        },
    }


@admin.register(Booking)
class BookingAdminClass(ModelAdmin):
    list_display = ["user", "movie", "show_time", "seats"]
    search_fields = ("user__username", "movie__title")
    list_filter = ("movie", "show_time")

    unfold_enabled = True
    compressed_fields = True
    warn_unsaved_form = True

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }
