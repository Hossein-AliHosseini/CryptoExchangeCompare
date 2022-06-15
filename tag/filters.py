from django.contrib.contenttypes.models import ContentType

import django_filters as filters

from tag.models import Tag


class ModelChoices:
    PERSON = 'Person'
    TRANSACTION = "Transaction"
    ACCOUNT = "Account"

    TYPES = (
        (ContentType.objects.get(app_label='user', model='person').id, "Person"),
        (ContentType.objects.get(app_label='exchange', model='transaction').id, 'Transaction'),
        (ContentType.objects.get(app_label='exchange', model='account').id, "Account")
    )


class TagFilter(filters.FilterSet):
    tag_title__icontains = filters.CharFilter(field_name='tag_title', lookup_expr='icontains', label='Tag Title')
    content_type = filters.ChoiceFilter(choices=ModelChoices.TYPES, label='Model Name')

    class Meta:
        model = Tag
        exclude = ("content_type", "object_id", "content_object", 'tag_title')
