from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create an engine to connect to your database
engine = create_engine('sqlite:///eqiisales.db')

Base = declarative_base()

class SalesItem(Base):
    """
    dataclass to store the data items for one unit of a sales item
    """
    __tablename__ = "rawsales"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    server = Column(String)
    seller = Column(String)
    salesdate = Column(String)
    description = Column(String)
    price = Column(String)
    absoluteprice = Column(String)
    numbought = Column(Integer)

    Base.metadata.create_all(bind=engine)

    def __init__(self, server, seller, sdate, desc, price, absoluteprice, numbought):
        self.server = server
        self.seller = seller
        self.salesdate = sdate
        self.description = desc
        self.price = price
        self.absoluteprice = absoluteprice
        self.numbought = numbought

    def __repr__(self):
        return f"({self.id} {self.server} {self.seller} {self.salesdate} {self.description} {self.price} {self.absoluteprice} {self.numbought})"
