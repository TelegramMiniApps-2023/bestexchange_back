from pydantic import BaseModel, Field

from general_models.schemas import SpecialDirectionModel


class CityModel(BaseModel):
    id: int = Field(alias='pk')
    # id: int
    name: str
    code_name: str

    class Config:
        json_schema_extra = {
            'examples': [
                {
                    'id': 0,
                    'name': 'string',
                    'code_name': 'string',
                }
            ]
        }


class CountryModel(BaseModel):
    # id: int = Field(alias='country__pk', json_schema_extra={'id', 1})
    # name: str = Field(alias='country__name')
    id: int = Field(alias='pk', json_schema_extra={'id', 1})
    name: str

    icon_url: str | None = Field(alias='country_flag')
    cities: list[CityModel] = Field(alias='city_list')

    # class Config:
    #     json_schema_extra = {
    #         'examples': [
    #             {
    #                 'id': 0,
    #                 'name': 'string',
    #             }
    #         ]
    #     }
    

class SpecialCashDirectionModel(SpecialDirectionModel):
    params: str
    fromfee: float | None