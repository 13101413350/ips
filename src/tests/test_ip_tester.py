import pytest
import aiohttp
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
    """测试有效 IP 的下载速度。"""
    async with aiohttp.ClientSession() as session:  # 明确创建 session
        result = await test_speed(session, "1.1.1.1")
        assert result is None or (isinstance(result, float) and result >= 0)
