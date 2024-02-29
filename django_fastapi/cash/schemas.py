from pydantic import BaseModel, Field

from general_models.schemas import SpecialDirectionModel, SpecialDirectionMultiModel


class MultipleName(BaseModel):
    ru: str = Field(alias='name')
    en: str = Field(alias='en_name')


class CityModel(BaseModel):
    id: int = Field(alias='pk')
    name: str
    code_name: str

    class Config:
        json_schema_extra = {
            'examples': [
                {
                    'id': 0,
                    'name': {
                        'name': 'string',
                        'en_name': 'string',
                    },
                    'code_name': 'string',
                }
            ]
        }


class RuEnCityModel(BaseModel):
    id: int = Field(alias='pk')
    name: MultipleName
    code_name: str

    class Config:
        json_schema_extra = {
            'examples': [
                {
                    'id': 0,
                    'name': {
                        'name': 'string',
                        'en_name': 'string',
                    },
                    'code_name': 'string',
                }
            ]
        }


class CountryModel(BaseModel):
    id: int = Field(alias='pk', json_schema_extra={'id', 1})
    name: str

    icon_url: str | None = Field(alias='country_flag')
    cities: list[CityModel] = Field(alias='city_list')


class RuEnCountryModel(BaseModel):
    id: int = Field(alias='pk', json_schema_extra={'id', 1})
    name: MultipleName

    icon_url: str | None = Field(alias='country_flag')
    cities: list[RuEnCityModel] = Field(alias='city_list')
    

class SpecialCashDirectionModel(SpecialDirectionModel):
    params: str
    fromfee: float | None


class SpecialCashDirectionMultiModel(SpecialDirectionMultiModel):
    params: str
    fromfee: float | None