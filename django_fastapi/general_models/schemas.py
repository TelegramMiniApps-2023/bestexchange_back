from pydantic import BaseModel


class ValuteModel(BaseModel):
    id: int
    name: str
    code_name: str
    icon_url: str | None


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