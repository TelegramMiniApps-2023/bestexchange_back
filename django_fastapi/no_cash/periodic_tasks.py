import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from general_models.utils.periodic_tasks import get_or_create_schedule

from .models import Exchange


def manage_periodic_task_for_create(exchange_pk: int,
                                    exchange_name: str,
                                    interval: int):
    '''
    Создание, изменение, остановка периодической задачи
    для создания готовых направлений обменника
    '''

    try:
        task = PeriodicTask.objects\
                            .get(name=f'{exchange_pk} no_cash task creation')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_pk} no_cash task creation',
                    task='create_no_cash_directions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            #остановить задачу периодических созданий готовых направлений в БД
            task.enabled = False
        else:
            task.enabled = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            task.interval = schedule
        task.save()


def manage_periodic_task_for_update(exchange_pk: int,
                                    exchange_name: str,
                                    interval: int):
    '''
    Создание, изменение, остановка периодической задачи
    для обновления готовых направлений обменника
    '''

    try:
        task = PeriodicTask.objects\
                                .get(name=f'{exchange_pk} no_cash task update')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_pk} no_cash task update',
                    task='update_no_cash_diretions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            #остановить задачу периодических обновлений
            task.enabled = False
             #сделать обменник неактивным из-за неактуальных данных
            exchange_active = False
        else:
            
            task.enabled = True
            exchange_active = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            task.interval = schedule
        Exchange.objects.filter(name=exchange_name).update(is_active=exchange_active)
        task.save()


def manage_periodic_task_for_parse_black_list(exchange_pk: int,
                                              exchange_name: str,
                                              interval: int):
    '''
    Создание, изменение, остановка периодической задачи
    для парсинга чёрного списка обменника
    '''

    try:
        task = PeriodicTask.objects\
                            .get(name=f'{exchange_pk} no_cash task black list')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(interval, IntervalSchedule.HOURS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_pk} no_cash task black list',
                    task='try_create_no_cash_directions_from_black_list',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if interval == 0:
            #остановить задачу периодического парсинга чёрного списка
            task.enabled = False
        else:
            task.enabled = True
            schedule = get_or_create_schedule(interval, IntervalSchedule.HOURS)
            task.interval = schedule
        task.save()