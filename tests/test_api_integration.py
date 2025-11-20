import pytest
from httpx import AsyncClient
from src.api.app import create_app

@pytest.mark.asyncio
async def test_status_summary_returns_engine_and_limit():
    app = create_app()

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/api/status/summary")

    assert response.status_code == 200
    data = response.json()
    assert "engine" in data
    assert "daily_limit" in data
