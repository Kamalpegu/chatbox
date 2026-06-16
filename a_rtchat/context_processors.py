from .models import ChatGroup


def groupchats(request):
    if not request.user.is_authenticated:
        return {}

    return {
        'groupchats': ChatGroup.objects.filter(groupchat_name__isnull=False).exclude(groupchat_name=''),
    }
