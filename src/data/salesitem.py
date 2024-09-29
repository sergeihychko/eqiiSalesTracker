from dataclasses import dataclass, field


@dataclass(order=True)
class SalesItem:
    server: str
    seller: str
    salesdate: str
    description: str
    price: str
    absoluteprice: str
    numbought: int = field(default=1)

