import asyncio
import aiohttp
import pythonping
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from src.config import TEST_URL, PING_COUNT, TIMEOUT, MIN_SPEED, MAX_DELAY, ISP_REGIONS


async def test_speed(session, ip):
    """异步测试 IP 下载速度。

    Args:
        session: aiohttp.ClientSession 对象。
        ip: 测试的 IP 地址。

    Returns:
        float: 下载速度（MB/s），失败时返回 None。
    """
    try:
        start_time = asyncio.get_event_loop().time()
        async with session.get(TEST_URL, timeout=5) as response:
            if response.status == 200:
                content = await response.read()
                speed = len(content) / (asyncio.get_event_loop().time() - start_time) / 1024 / 1024
                return speed if speed >= MIN_SPEED else None
    except Exception as e:
        logging.error(f"测试速度 {ip} 失败：{e}")
        return None


def test_delay(ip):
    """测试 IP 延迟。

    Args:
        ip: 测试的 IP 地址。

    Returns:
        float: 平均延迟（ms），失败时返回 None。
    """
    try:
        response = pythonping.ping(ip, count=PING_COUNT, timeout=TIMEOUT)
        if response.success():
            return response.rtt_avg_ms
        return None
    except Exception as e:
        logging.error(f"测试延迟 {ip} 失败：{e}")
        return None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_ip_info(ip, session, semaphore):
    """获取 IP 地理位置和 ISP 信息，限制请求速率。

    Args:
        ip: 测试的 IP 地址。
        session: aiohttp.ClientSession 对象。
        semaphore: asyncio.Semaphore 对象，限制并发。

    Returns:
        dict: 包含国家、ISP 的字典，失败时返回 None。
    """
    async with semaphore:
        try:
            async with session.get(f"http://ip-api.com/json/{ip}") as response:
                if response.status == 200:
                    data = await response.json()
                    return {"country": data.get("country", ""), "isp": data.get("isp", "")}
                return None
        except Exception as e:
            logging.error(f"获取 IP 信息 {ip} 失败：{e}")
            return None


async def test_ip(ip, session, isp, semaphore):
    """测试单个 IP 的速度、延迟和地区。

    Args:
        ip: 测试的 IP 地址。
        session: aiohttp.ClientSession 对象。
        isp: ISP 标识（cf, cu, cm, ct）。
        semaphore: asyncio.Semaphore 对象。

    Returns:
        dict: 包含 IP、延迟、速度、地区、ISP 的字典，失败时返回 None。
    """
    try:
        ip_info = await get_ip_info(ip, session, semaphore)
        if not ip_info or ip_info["country"] not in ISP_REGIONS[isp]:
            return None

        delay = test_delay(ip)
        if delay is None or delay > MAX_DELAY:
            return None

        speed = await test_speed(session, ip)
        if speed is None:
            return None

        return {
            "ip": ip,
            "delay": delay,
            "speed": speed,
            "country": ip_info["country"],
            "isp": ip_info["isp"]
        }
    except Exception as e:
        logging.error(f"测试 IP {ip} 失败：{e}")
        return None


async def test_ips(ips, isp, ip_count):
    """异步测试 IP 列表，限制请求速率。

    Args:
        ips: IP 地址列表。
        isp: ISP 标识。
        ip_count: 返回的优选 IP 数量。

    Returns:
        list: 排序后的优选 IP 列表。
    """
    results = []
    semaphore = asyncio.Semaphore(45)  # 限制 ip-api.com 请求速率
    async with aiohttp.ClientSession() as session:
        tasks = [test_ip(ip, session, isp, semaphore) for ip in ips]
        for future in asyncio.as_completed(tasks):
            result = await future
            if result:
                results.append(result)
    return sorted(results, key=lambda x: (x["delay"], -x["speed"]))[:ip_count]
