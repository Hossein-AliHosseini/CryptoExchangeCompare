import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

from .forms import PersonTagForm
from .models import Tag
from .filters import TagFilter


def person_tag(request):
    if request.method == "POST":
        form = PersonTagForm(request.POST)
        if form.is_valid():
            person = form.cleaned_data['person']
            tag_title = form.cleaned_data['tag_title']
            if not tag_title:
                return render(request, 'tag/profile.html', {"form": form,
                                                            "qs": person.tags.all()})
            Tag.objects.create(content_object=person, object_id=person.pk, tag_title=tag_title)
            return render(request, 'tag/profile.html', {"form": form,
                                                        "qs": person.tags.all()})
    else:
        form = PersonTagForm()
        return render(request, 'tag/profile.html', {"form": form})


def tag_filter(request):
    f = TagFilter(request.GET, queryset=Tag.objects.all())
    qs = f.qs.values_list('tag_title', flat=True)
    model_id = request.GET.get('content_type', None)
    if model_id:
        model = ContentType.objects.get(id=model_id)
        model = apps.get_model(model.app_label + "." + model.model)
        qs = model.objects.filter(tags__tag_title__in=qs)
        return render(request, 'tag/tag_filter.html', {"filter": f,
                                                       "qs": qs.distinct(),
                                                       "type_check": True,
                                                       "fields": [f.name for f in model._meta.get_fields()]})
    return render(request, 'tag/tag_filter.html', {"filter": f,
                                                   "qs": f.qs.values('tag_title'),
                                                   "type_check": False})


def tag_title_autocomplete(request):
    q = request.GET.get('term', '')
    res = list()
    queryset = Tag.objects.filter(tag_title__icontains=q)
    for query in queryset:
        res.append(query.tag_title)
    data = json.dumps(res)
    mimetypes = 'application/json'
    return HttpResponse(data, mimetypes)
