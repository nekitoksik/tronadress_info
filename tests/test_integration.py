import pytest
from fastapi import status
from app.api.schemas.schemas import AddressInfoRequest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_get_address_info(client, mocker):
    # Мокаем AsyncTron и его методы
    mock_tron = mocker.patch("app.api.services.services.AsyncTron")
    mock_instance = mock_tron.return_value
    
    # Настраиваем асинхронные моки
    mock_instance.is_address.return_value = True
    mock_instance.get_account = AsyncMock(return_value={"some": "data"})
    mock_instance.get_account_balance = AsyncMock(return_value=1000000.0)
    mock_instance.get_account_resource = AsyncMock(return_value={
        "freeNetLimit": 5000,
        "TotalEnergyLimit": 10000
    })

    test_data = {"address": "TT5iK8oqGEyRKJAnRwrLSZ4fM5y77F2LNT"}
    
    response = client.post("/api/v1/address-info", json=test_data)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["address"] == test_data["address"]
    assert response_data["balance"] == 1000000
    assert response_data["bandwith"] == 5000
    assert response_data["energy"] == 10000