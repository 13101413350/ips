import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from src.ip_tester import test_delay, test_speed


def test_delay_valid_ip():
    """测试有效 IP 的延迟。"""
    result = test_delay("1.1.1.1")
    assert result is None or (isinstance(result, float) and result >= 0)


def test_delay_invalid_ip():
    """测试无效 IP 的延迟。"""
    result = test_delay("999.999.999.999")
    assert result is None


@pytest.mark.asyncio
async def test_speed_valid_ip():
    """测试有效 IP 的下载速度，使用模拟响应。"""
    with patch("aichttp.ClientSession.get", new=AsyncMock()) as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"0" * 5_000_000)  # 模拟 5MB 数据
        mock_get.return_value.__aenter__.return_value = mock_response
        async with aiohttp.ClientSession() as session:
            result = await test_speed(session, "1.1.1.1")
            assert result is None or (isinstance(result, float) and result >= 0)
