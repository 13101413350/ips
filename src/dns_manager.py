import requests
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from src.config import CF_API_TOKEN, CF_ZONE_ID, CF_EMAIL


headers = {
    "X-Auth-Email": CF_EMAIL,
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json",
}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), after=lambda retry_state: logging.info(f"DNS 更新重试 {retry_state.attempt_number}/3"))
def update_dns_record(domain, ips):
    """更新 Cloudflare DNS A 记录。

    Args:
        domain: 要更新的域名。
        ips: 优选 IP 列表。

    Returns:
        bool: 更新成功返回 True，否则 False。
    """
    base_url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}"
    url = f"{base_url}/dns_records"
    try:
        # 获取当前 DNS 记录
        response = requests.get(url, headers=headers, params={"name": domain}, timeout=5)
        response.raise_for_status()
        records = response.json().get("result", [])
        logging.info(f"获取 {domain} DNS 记录：{len(records)} 条")

        # 删除旧记录
        for record in records:
            requests.delete(f"{url}/{record['id']}", headers=headers, timeout=5)
            logging.info(f"删除 DNS 记录 {domain} -> {record['content']}")

        # 添加新 A 记录
        for ip in ips:
            data = {
                "type": "A",
                "name": domain,
                "content": ip,
                "ttl": 1,
                "proxied": True
            }
            response = requests.post(url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            logging.info(f"添加 DNS 记录 {domain} -> {ip}")
        return True
    except Exception as e:
        logging.error(f"更新 DNS 记录 {domain} 失败：{e}")
        return False
