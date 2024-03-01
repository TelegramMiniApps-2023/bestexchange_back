from django.core.cache import cache
from django.contrib.auth.models import User

from partners.models import CustomUser


def get_or_set_user_account_cache(user: User):
    if not (account_user := cache.get(f'account_user_{user.pk}', False)):
        account_user = CustomUser.objects\
                            .select_related('exchange', 'user')\
                            .filter(user=user).get()
        cache.set(f'account_user_{user.pk}', account_user, 20)
    return account_user


def set_user_account_cache(account_user: CustomUser):
        cache.set(f'account_user_{account_user.user.pk}', account_user, 20)