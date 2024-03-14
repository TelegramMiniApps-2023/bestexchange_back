# from django_celery_beat.models import PeriodicTask


# def manage_popular_count_direction_task(fields_to_update: dict):
#     try:
#         task = PeriodicTask.objects.get(name='update_popular_count_direction_time_task')
#     except PeriodicTask.DoesNotExist:
#         pass
#     else:
#         amount = fields_to_update['amount']
#         unit_time = fields_to_update['unit_time']
#         schedule = get_or_create_schedule(amount,
#                                           UNIT_TIME_CHOICES[unit_time])
#         task.interval = schedule
#         task.save()