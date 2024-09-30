from dataclasses import dataclass, field

@dataclass(order=True)
class SalesItem:
    """
    dataclass to store the data items for one unit of a sales item
    """
    server: str
    seller: str
    salesdate: str
    description: str
    price: str
    absoluteprice: str
    numbought: int = field(default=1)
