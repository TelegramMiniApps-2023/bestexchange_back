from cash.models import Country
from cash.schemas import MultipleName

from general_models.utils.endpoints import try_generate_icon_url


def get_available_countries(cities):

    '''
    Возвращает QuerySet доступных стран с необходимыми данными
    '''

    country_names = sorted({city.country.name for city in cities})
    
    countries = Country.objects.filter(name__in=country_names)\
                                .prefetch_related('cities').all()

    for country in countries:
        country.city_list = list(filter(lambda el: el.is_parse == True,
                                        country.cities.all()))
        for city in country.city_list:
            city.name = MultipleName(name=city.name,
                                     en_name=city.en_name)
        
        country.country_flag = try_generate_icon_url(country)

        country.name = MultipleName(name=country.name,
                                   en_name=country.en_name)
    
    return countries