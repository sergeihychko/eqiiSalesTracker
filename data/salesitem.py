import uuid
from dataclasses import dataclass, field


@dataclass(order=True)
class SalesItem:
    server: str
    seller: str
    salesdate: str
    description: str
    price: str
    absoluteprice: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

