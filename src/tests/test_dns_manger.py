import pytest
from unittest.mock import patch
from src.dns_manager import update_dns_record


def test_update_dns_record_success():
    """测试成功更新 DNS 记录。"""
    with patch('requests.get') as mock_get, patch('requests.delete') as mock_delete, patch('requests.post') as mock_post:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": []}
        mock_post.return_value.status_code = 200
        result = update_dns_record("test.example.com", ["1.1.1.1"])
        assert result is True


def test_update_dns_record_failure():
    """测试 DNS 记录更新失败。"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {"result": []}
        mock_get.return_value.raise_for_status.side_effect = Exception("API 错误")
        result = update_dns_record("test.example.com", ["1.1.1.1"])
        assert result is False
