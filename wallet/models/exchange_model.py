from pydantic import BaseModel, ConfigDict

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
}

