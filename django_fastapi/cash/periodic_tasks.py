import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from general_models.utils.periodic_tasks import get_or_create_schedule


def manage_periodic_task_for_create(exchange_name: str, interval: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} cash task creation')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} cash task creation',
                    task='create_cash_directions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            task.enabled = False
        else:
            task.enabled = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            task.interval = schedule
        task.save()


def manage_periodic_task_for_update(exchange_name: str, interval: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} cash task update')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} cash task update',
                    task='update_cash_diretions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            task.enabled = False
        else:
            task.enabled = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            task.interval = schedule
        task.save()


def manage_periodic_task_for_parse_black_list(exchange_name: str, interval: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} cash task black list')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.HOURS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} cash task black list',
                    task='try_create_cash_directions_from_black_list',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            task.enabled = False
        else:
            task.enabled = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.HOURS)
            task.interval = schedule
        task.save()