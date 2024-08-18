from pydantic import BaseModel

from enum import Enum

class Currency(str, Enum):
    THB = "THB"
    USD = "USD"
    CNY = "CNY"
    JPY = "JPY"

class BaseExchange(BaseModel):
    from_currency: Currency = Currency.THB
    to_currency: Currency
    amount: float

EXCHANGE_RATES = {
    "USD": 34.99,
    "CNY": 4.88,
    "JPY": 0.23,  
    "LAK": 637.52,
    "MMK": 60.63,
    "VND": 724.20,
    "BND": 0.03797,
    "SGD": 0.03809,
    "PHP": 1.6534,
    "KRW": 39.012
}

