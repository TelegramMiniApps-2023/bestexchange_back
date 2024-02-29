# from django.core.management.base import BaseCommand, CommandError

# from django_celery_beat.models import IntervalSchedule, PeriodicTask

# from general_models.utils.periodic_tasks import get_or_create_schedule


# # python manage.py periodic_task_for_check_direction_on_active в docker-compose файле
# # Команда для создания периодической задачи, которая проверяет партнёрские направления
# # на активность, если направление не изменялось более 3 дней,
# # направление становится неактивным


# class Command(BaseCommand):
#     print('Creating periodic task for check partner directions on active...')

#     def handle(self, *args, **kwargs):
#         try:
#             schedule = get_or_create_schedule(60, IntervalSchedule.SECONDS)
#             PeriodicTask.objects.create(
#                     interval=schedule,
#                     name='check_update_time_for_directions_task',
#                     task='check_update_time_for_directions',
#                     )
#         except Exception as ex:
#             print(ex)
#             raise CommandError('Initalization failed.')