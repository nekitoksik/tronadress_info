import os
from fastapi import HTTPException

from app.api.database import async_session_maker
from tronpy import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider

from sqlalchemy import select
from app.api.models.models import RequestHistory
from app.api.schemas.schemas import AddressInfoResponse, AddressInfoRequest
from app.api.config import settings

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TronAddressService:
    model = RequestHistory

    @classmethod
    async def get_requests_history(cls, skip: int = 0, limit: int = 10):
        async with async_session_maker() as session:
            try:
                query = select(RequestHistory).order_by(
                    RequestHistory.created_at.desc()
                ).offset(skip).limit(limit)

                result = await session.execute(query)
                return result.scalars().all()
            
            except Exception as e:
                logger.error(f"Error: {e}")
                raise HTTPException(status_code=500, detail=str(e))


    @classmethod
    async def get_address_info(cls, address_request: AddressInfoRequest) -> AddressInfoResponse:
        async with async_session_maker() as session:
            address = address_request.address
            
            try:
                tron_api_key = settings.TRONGRID_API_KEY
                headers = {"TRON-PRO-API-KEY": tron_api_key}
                tron_client = AsyncTron(
                    AsyncHTTPProvider(
                        "https://api.trongrid.io",
                        api_key=tron_api_key
                    )
                )

                if not tron_client.is_address(address):
                    raise HTTPException(status_code=400, detail="Invalid Tron address")
            
                account = await tron_client.get_account(address)
                balance = await tron_client.get_account_balance(address)
                resources = await tron_client.get_account_resource(address)

                print(balance)
                print(resources)
                print(resources.get("TotalEnergyLimit", 0))
                query = RequestHistory(address=address)
                session.add(query)

                await session.commit()
                await session.refresh(query)
                logger.info(f"Запрос для кошелька {address}")

                response = AddressInfoResponse(address=address, bandwith=resources.get("freeNetLimit", 0), energy=resources.get("TotalEnergyLimit", 0), balance=balance) 
                return response
                

            except Exception as e:
                logger.error(f"Error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
            



            # if not is_address(address):
            #     raise HTTPException(status_code=400, detail="Invalid Tron address")
            
            # try:
            #     async with AsyncTron(
            #         AsyncHTTPProvider(
            #             endpoint_uri=os.getenv("TRON_PROVIDER", "https://api.trongrid.io"),
            #             api_key=os.getenv("TRON_API_KEY")
            #         )
            #     ) as client:
                    
            #         balance_sun = await client.get_account_asset_balance(address)
            #         balance_trx = balance_sun / 1_000_000

            #         account_net = await client.get_acc

