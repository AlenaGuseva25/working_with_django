from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='is_moderator')
def is_moderator(user):
    try:
        moderator_group = Group.objects.get(name='Модератор продуктов')
        return moderator_group in user.groups.all()
    except Group.DoesNotExist:
        return False