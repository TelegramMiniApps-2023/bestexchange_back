from parnters.models import Direction


def get_in_count(direction):
        actual_course = direction.direction.actual_course
        if actual_course < 1:
            convert_course = 1 / actual_course
            res = convert_course + (convert_course * direction.percent / 100) + direction.fix_amount
        else:
            res = 1
        return round(res, 2)

def get_out_count(direction):
        actual_course = direction.direction.actual_course
        if actual_course < 1:
            res = 1
        else:
            res = actual_course - (actual_course * direction.percent / 100) - direction.fix_amount
        return round(res, 2)

def get_partner_directions(city: str,
                           valute_from: str,
                           valute_to: str):
    direction_name = valute_from + ' -> ' + valute_to
    directions = Direction.objects\
                            .select_related('exchange', 'direction')\
                            .prefetch_related('cities')\
                            .filter(direction__display_name=direction_name,
                                    cities__code_name=city)

    for direction in directions:
        direction.valute_from = valute_from
        direction.valute_to = valute_to
        direction.in_count = get_in_count(direction)
        direction.out_count = get_out_count(direction)
        direction.min_amount = 'Не установлено'
        direction.max_amount = 'Не установлено'
        direction.params = 'Не установлено'
        direction.fromfee = direction.percent

    return directions