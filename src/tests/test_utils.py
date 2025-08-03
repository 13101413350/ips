import pytest
from unittest.mock import patch
from src.utils import get_ip_list, check_system_resources


def test_get_ip_list():
    """测试生成 IP 列表。"""
    ip_ranges = ["192.168.1.0/30"]
    test_count = 2
    ip_list = get_ip_list(ip_ranges, test_count)
    assert len(ip_list) <= test_count
    assert all(ip.startswith("192.168.1.") for ip in ip_list)


def test_check_system_resources_low_usage():
    """测试系统资源充足情况。"""
    with patch('psutil.cpu_percent', return_value=50), patch('psutil.virtual_memory') as mock_mem:
        mock_mem.return_value.percent = 60
        result = check_system_resources()
        assert result is True


def test_check_system_resources_high_usage():
    """测试系统资源紧张情况。"""
    with patch('psutil.cpu_percent', return_value=90), patch('psutil.virtual_memory') as mock_mem:
        mock_mem.return_value.percent = 85
        result = check_system_resources()
        assert result is False
