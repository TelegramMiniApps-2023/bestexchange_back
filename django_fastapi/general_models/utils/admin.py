from typing import Any

from general_models.models import BaseExchange


class ReviewAdminMixin:
        def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
            if not isinstance(obj, BaseExchange):
                obj.moderation = obj.status == 'Опубликован'
            return super().save_model(request, obj, form, change)
        
        def save_formset(self, request: Any, form: Any, formset: Any, change: Any) -> None:
            instances = formset.save(commit=False)
            for instance in instances:
                if hasattr(instance, 'moderation'):
                    instance.moderation = instance.status == 'Опубликован'
                    instance.save()
            return super().save_formset(request, form, formset, change)