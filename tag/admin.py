from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin, GenericStackedInline
from django import forms

from .models import Tag


class TagInLine(GenericStackedInline):
    model = Tag


class TagAdmin(admin.ModelAdmin):
    inlines = [TagInLine, ]


admin.site.register(Tag, TagAdmin)
