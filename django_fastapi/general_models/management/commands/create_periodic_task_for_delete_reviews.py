from django.core.management.base import BaseCommand, CommandError

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from general_models.utils.periodic_tasks import get_or_create_schedule


class Command(BaseCommand):
    print('Creating Task for delete cancel reviews')

    def handle(self, *args, **kwargs):
        try:
            schedule = get_or_create_schedule(1, IntervalSchedule.MINUTES)
            PeriodicTask.objects.create(
                interval=schedule,
                name='task for delete cancel reviews',
                task='delete_cancel_reviews',
            )
            pass
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')