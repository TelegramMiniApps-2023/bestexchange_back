from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission


def create_group(group_name: str,
                 models: tuple):
    seo_group, _ = Group.objects.get_or_create(name=group_name)
    
    for model in models:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        seo_group.permissions.add(*permissions)