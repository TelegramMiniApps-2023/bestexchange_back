from django.conf import settings

from django_celery_beat.models import PeriodicTask

from general_models.utils.periodic_tasks import get_or_create_schedule
from general_models.utils.base import UNIT_TIME_CHOICES


def edit_time_for_task_check_directions_on_active(task: str,
                                                  fields_to_update: dict):
    try:
        # task = PeriodicTask.objects.get(name='check_update_time_for_directions_task')
        task = PeriodicTask.objects.get(name=task)
    except PeriodicTask.DoesNotExist:
        pass
    else:
        amount = fields_to_update['amount']
        unit_time = fields_to_update['unit_time']
        schedule = get_or_create_schedule(amount,
                                          UNIT_TIME_CHOICES[unit_time])
        task.interval = schedule
        task.save()


    