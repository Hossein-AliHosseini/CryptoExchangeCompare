from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag
from .models import Transaction, Account


class TagInLine(GenericStackedInline):
    model = Tag


class TagAdmin(admin.ModelAdmin):
    inlines = [TagInLine, ]


admin.site.register(Transaction, TagAdmin)
admin.site.register(Account, TagAdmin)
