import pytest
from sqlalchemy import select
from app.api.models.models import RequestHistory
from app.api.schemas.schemas import AddressInfoRequest
from app.api.services.services import TronAddressService
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_db_record_creation(session):
    # Мокаем только внешние зависимости, не трогая сессию
    with patch("app.api.services.services.AsyncTron") as mock_tron:
        mock_instance = mock_tron.return_value
        mock_instance.is_address.return_value = True
        mock_instance.get_account = AsyncMock(return_value={})
        mock_instance.get_account_balance = AsyncMock(return_value=0)
        mock_instance.get_account_resource = AsyncMock(return_value={})

        test_address = "TT5iK8oqGEyRKJAnRwrLSZ4fM5y77F2LNT"
        test_request = AddressInfoRequest(address=test_address)
        
        # Используем нашу тестовую сессию
        with patch(
            "app.api.services.services.async_session_maker",
            return_value=MagicMock(
                __aenter__=AsyncMock(return_value=session),
                __aexit__=AsyncMock(return_value=None)
            )
        ):
            try:
                await TronAddressService.get_address_info(test_request)
                
                # Проверяем, что запись создана
                query = select(RequestHistory).where(RequestHistory.address == test_address)
                result = await session.execute(query)
                records = result.scalars().all()
                
                assert len(records) == 1
                assert records[0].address == test_address
            except Exception as e:
                pytest.fail(f"Test failed with exception: {str(e)}")