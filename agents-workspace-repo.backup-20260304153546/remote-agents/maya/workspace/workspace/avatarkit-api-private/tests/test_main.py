"""
AvatarKit API 测试
"""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ==================== 健康检查 ====================

@pytest.mark.asyncio
async def test_health_check(client):
    """测试健康检查端点"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "services" in data


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """测试根端点"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


# ==================== 定价信息 ====================

@pytest.mark.asyncio
async def test_pricing_endpoint(client):
    """测试定价端点"""
    response = await client.get("/v1/pricing")
    assert response.status_code == 200
    data = response.json()
    assert "currency" in data
    assert "services" in data
    assert "free_tier" in data


# ==================== 认证 ====================

@pytest.mark.asyncio
async def test_register_missing_fields(client):
    """测试注册缺少字段"""
    response = await client.post("/v1/auth/register", json={})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_login_missing_fields(client):
    """测试登录缺少字段"""
    response = await client.post("/v1/auth/login", json={})
    assert response.status_code == 422  # Validation error


# ==================== 未认证访问 ====================

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """测试未认证访问受保护端点"""
    response = await client.get("/v1/user/profile")
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_unauthorized_avatar_list(client):
    """测试未认证获取形象列表"""
    response = await client.get("/v1/avatars")
    assert response.status_code == 401  # Unauthorized


# ==================== 套餐列表 ====================

@pytest.mark.asyncio
async def test_packages_endpoint(client):
    """测试获取充值套餐（无需认证）"""
    response = await client.get("/v1/orders/packages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
