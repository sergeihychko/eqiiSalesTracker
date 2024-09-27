from dataclasses import dataclass
from datetime import datetime


@dataclass
class SalesItem:
    server: str
    seller: str
    salesdate: datetime
    description: str
    price: str
    absoluteprice: float

