from unittest.mock import patch
from src.main import main


@patch('src.utils.check_system_resources', return_value=True)
@patch('src.utils.get_ip_list', return_value=["1.1.1.1"])
@patch('src.ip_tester.test_ips', return_value=[{
    "ip": "1.1.1.1",
    "delay": 10,
    "speed": 10,
    "country": "Hong Kong",
    "isp": "Cloudflare"
}])
@patch('src.dns_manager.update_dns_record', return_value=True)
def test_main_success(mock_dns, mock_test_ips, mock_get_ip, mock_resources):
    """测试主函数成功执行。"""
    with patch('logging.info') as mock_log:
        main()
        assert mock_resources.called
        assert mock_get_ip.called
        assert mock_test_ips.called
        assert mock_dns.called
        mock_log.assert_any_call("开始 Cloudflare 优化")


@patch('src.utils.check_system_resources', return_value=False)
def test_main_resource_failure(mock_resources):
    """测试主函数因资源不足退出。"""
    with patch('logging.error') as mock_log:
        main()
        mock_log.assert_called_with("系统资源不足，退出")
