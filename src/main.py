import asyncio
import logging
from src.config import DOMAINS, CF_IP_RANGES, TEST_COUNT
from src.utils import get_ip_list, check_system_resources
from src.ip_tester import test_ips
from src.dns_manager import update_dns_record


def main():
    """优化 Cloudflare DNS，使用优选 IP。"""
    logging.info("开始 Cloudflare 优化")
    if not check_system_resources():
        logging.error("系统资源不足，退出")
        return

    ip_list = get_ip_list(CF_IP_RANGES, TEST_COUNT)
    loop = asyncio.get_event_loop()

    for domain, ip_count in DOMAINS.items():
        isp = domain.split(".")[0]
        logging.info(f"测试 {domain} ({isp}) 的优选 IP")

        # 异步测试 IP
        results = loop.run_until_complete(test_ips(ip_list, isp, ip_count))
        if not results:
            logging.error(f"未找到适合 {domain} 的 IP")
            continue

        # 记录结果
        logging.info(f"{domain} 的优选 IP：")
        for result in results:
            logging.info(
                f"IP: {result['ip']}, 延迟: {result['delay']}ms, "
                f"速度: {result['speed']:.2f}MB/s, 地区: {result['country']}"
            )

        # 更新 DNS
        ips = [result["ip"] for result in results]
        if update_dns_record(domain, ips):
            logging.info(f"{domain} DNS 记录更新完成")
        else:
            logging.error(f"{domain} DNS 记录更新失败")


if __name__ == "__main__":
    main()
