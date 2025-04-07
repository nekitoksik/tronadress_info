from fastapi import APIRouter
from app.api.schemas.schemas import AddressInfoResponse, AddressInfoRequest, RequestHistoryERsponse

from app.api.services.services import TronAddressService
from typing import List

router = APIRouter(
    prefix="/api/v1",
    tags=["Получение Информации по адресу кошелька"]
)

@router.post("/address-info", response_model=AddressInfoResponse)
async def get_address_info(address_request: AddressInfoRequest) -> AddressInfoResponse:
    return await TronAddressService.get_address_info(address_request)


@router.get("/request-history/", response_model=List[RequestHistoryERsponse])
async def get_request_history(skip: int = 0, limit: int = 10):
    return await TronAddressService.get_requests_history(skip, limit)

