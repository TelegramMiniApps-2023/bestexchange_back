from django.db.models import Count, Q

from partners.models import Direction


def get_in_count(direction):
        if direction is None:
            return 0
        actual_course = direction.direction.actual_course
        if actual_course < 1:
            convert_course = 1 / actual_course
            res = convert_course + (convert_course * direction.percent / 100) + direction.fix_amount
        else:
            res = 1
        return round(res, 2)


def get_out_count(direction):
        if direction is None:
            return 0
        actual_course = direction.direction.actual_course
        if actual_course < 1:
            res = 1
        else:
            res = actual_course - (actual_course * direction.percent / 100) - direction.fix_amount
        return round(res, 2)


def get_course_count(direction):
        if direction is None:
            return 0
        actual_course = direction.direction.actual_course
        return actual_course if actual_course is not None else 0


def get_partner_directions(city: str,
                           valute_from: str,
                           valute_to: str):
    direction_name = valute_from + ' -> ' + valute_to
    review_count_filter = Count('city__exchange__reviews',
                                filter=Q(city__exchange__reviews__moderation=True))
    directions = Direction.objects\
                            .select_related('direction',
                                            'city',
                                            'city__city',
                                            'city__exchange')\
                            .annotate(review_count=review_count_filter)\
                            .filter(direction__display_name=direction_name,
                                    city__city__code_name=city,
                                    is_active=True,
                                    city__exchange__partner_link__isnull=False)

    for direction in directions:
        direction.exchange = direction.city.exchange
        direction.valute_from = valute_from
        direction.valute_to = valute_to
        direction.in_count = get_in_count(direction)
        direction.out_count = get_out_count(direction)
        direction.min_amount = 'Не установлено'
        direction.max_amount = 'Не установлено'
        direction.params = 'Не установлено'
        direction.fromfee = direction.percent

    return directions