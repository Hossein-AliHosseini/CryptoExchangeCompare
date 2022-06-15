from django import template

register = template.Library()


def getattrs(value, arg):
    if arg != 'tags':
        return getattr(value, arg)
    return [s for s in getattr(value, arg).values_list('tag_title', flat=True)]


register.filter('getattrs', getattrs)
