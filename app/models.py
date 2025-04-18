from pydantic import BaseModel
from decimal import Decimal
from datetime import date, time
from uuid import UUID

class Item(BaseModel):
    shortDescription: str
    price: Decimal

class Receipt(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    items: list[Item]
    total: Decimal

class ProcessResponse(BaseModel):
    id: UUID

class PointsResponse(BaseModel):
    points: int   