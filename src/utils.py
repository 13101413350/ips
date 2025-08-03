import logging
import ipaddress
import random
import psutil


# 配置日志
logging.basicConfig(
    filename="cloudflare-optimizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_ip_list(ip_ranges, test_count):
    """从 CIDR 范围生成随机 IP 列表。

    Args:
        ip_ranges: IP 段列表。
        test_count: 测试的 IP 数量。

    Returns:
        list: 随机 IP 列表。
    """
    ip_list = []
    for cidr in ip_ranges:
        network = ipaddress.ip_network(cidr)
        ip_count = min(test_count, network.num_addresses)
        ip_list.extend(str(ip) for ip in random.sample(list(network.hosts()), ip_count))
    logging.info(f"生成了 {len(ip_list)} 个 IP")
    return ip_list


def check_system_resources():
    """检查系统 CPU 和内存使用情况。

    Returns:
        bool: 如果资源充足返回 True，否则 False。
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    if cpu_usage > 80 or mem.percent > 80:
        logging.warning(f"系统资源紧张：CPU {cpu_usage}%，内存 {mem.percent}%")
        return False
    return True
