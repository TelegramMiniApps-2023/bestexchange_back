from datetime import datetime

from general_models.utils.base import get_actual_datetime

from cash.models import City

from partners.models import Direction


def make_city_active(obj: City):
    if not obj.is_parse:
        obj.is_parse = True
        obj.save()


def update_field_time_update(obj: Direction, update_fields: set):
     obj.time_update = datetime.now()
     update_fields.add('time_update')
     
     if not obj.is_active:
          obj.is_active = True
          update_fields.add('is_active')