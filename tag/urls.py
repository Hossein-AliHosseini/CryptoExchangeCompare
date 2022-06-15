from django.urls import path

from .views import person_tag, tag_title_autocomplete, tag_filter

urlpatterns = [
    path('person-tag/', person_tag, name='person-tag'),
    path('tag-title-autocomplete/', tag_title_autocomplete, name='tag-title-autocomplete'),
    path('tag-filter/', tag_filter, name='tag-filter'),
]
