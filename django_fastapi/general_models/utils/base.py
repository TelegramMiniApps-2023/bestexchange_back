from datetime import datetime, timedelta

from django_celery_beat.models import IntervalSchedule

from general_models.models import PartnerTimeUpdate


UNIT_TIME_CHOICES = {
    'SECOND': IntervalSchedule.SECONDS,
    'MINUTE': IntervalSchedule.MINUTES,
    'HOUR': IntervalSchedule.HOURS,
    'DAY': IntervalSchedule.DAYS,
    }


def get_actual_datetime():
    return datetime.now() + timedelta(hours=9)


def get_timedelta():
    time_live_obj = PartnerTimeUpdate.objects\
                                        .get(name='Управление временем жизни направлений')
    amount = time_live_obj.amount
    unit_time = time_live_obj.unit_time

    match unit_time:
        case 'SECOND':
            time_delta = timedelta(seconds=amount)
        case 'MINUTE':
            time_delta = timedelta(minutes=amount)
        case 'HOUR':
            time_delta = timedelta(hours=amount)
        case 'DAY':
            time_delta = timedelta(days=amount)
    
    return time_delta