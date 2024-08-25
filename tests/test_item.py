import pytest
from httpx import AsyncClient
from wallet.models.user_model import Token

import json

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, token_user1: Token):
    create_response = await client.post(
        "/items",
        json={
            "name": "Test Item",
            "description": "A description for the test item.",
            "price": 0.12,
            "tax": 0.12,
            "user_id": token_user1.user_id,
        },
        headers={"Authorization": f"Bearer {token_user1.access_token}"}
    )
    create_response.json()
    
@pytest.mark.asyncio
async def test_read_items(client: AsyncClient, token_user1: Token):
    list_response = await client.get(
        "/items",
        headers={"Authorization": f"Bearer {token_user1.access_token}"}
    )

    assert list_response.status_code == 200
    data = list_response.json()
    assert "items" in data
    assert "page" in data
    assert "page_count" in data
    assert "size_per_page" in data

@pytest.mark.asyncio
async def test_read_item(client: AsyncClient, token_user1: Token):
    item_id = 1
    get_response = await client.get(
        f"/items/{item_id}",
        headers={"Authorization": f"Bearer {token_user1.access_token}"}
    )

    assert get_response.status_code == 404
    data = get_response.json()
    assert "detail" in data
    assert data["detail"] == "Item not found"

