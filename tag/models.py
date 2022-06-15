from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Tag(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="content_type_tags", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    tag_title = models.SlugField()

    def __str__(self):
        return self.tag_title

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
