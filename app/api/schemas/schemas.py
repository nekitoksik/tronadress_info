from datetime import datetime
from pydantic import BaseModel

class AddressInfoRequest(BaseModel):
    address: str

class AddressInfoResponse(BaseModel):
    address: str
    bandwith: int
    energy: int
    balance: float

class RequestHistoryERsponse(BaseModel):
    id: int
    address: str
    created_at: datetime

    class Config:
        from_attributes = True
