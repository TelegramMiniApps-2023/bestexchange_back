from pydantic import BaseModel, Field


#Схема валюты для отображения в json ответе
class ValuteModel(BaseModel):
    id: int
    name: str
    code_name: str
    icon_url: str | None


#Схема валюты для английской версии для отображения в json ответе
class EnValuteModel(BaseModel):
    id: int
    name: str = Field(alias='en_name')
    code_name: str
    icon_url: str | None


#Схема готового направления для отображения в json ответе
class SpecialDirectionModel(BaseModel):
    id: int
    name: str
    partner_link: str | None
    valute_from: str
    icon_valute_from: str | None
    valute_to: str
    icon_valute_to: str | None
    in_count: float
    out_count: float
    min_amount: str
    max_amount: str