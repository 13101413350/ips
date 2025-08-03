# Cloudflare 配置
CF_API_TOKEN = "Ja27PMUVqrF3xepsFFEIlEY26Wx7qNoVv5lECa42"  # 替换为你的 Cloudflare API Token
CF_ZONE_ID = "480cb4c06a1a00989322919d16e44267"  # 替换为你的 Zone ID
CF_EMAIL = "Linjinbin571@gmail.com"  # 替换为你的 Cloudflare 账户邮箱

# 域名配置
DOMAINS = {
    "cf.666731.xyz": 50,  # 全网域名，50 个优选 IP
    "cu.666731.xyz": 20,  # 中国联通，20 个优选 IP
    "cm.666731.xyz": 20,  # 中国移动，20 个优选 IP
    "ct.666731.xyz": 20   # 中国电信，20 个优选 IP
}

# 测试参数
TEST_COUNT = 200  # 测试 IP 数量
PING_COUNT = 4    # 每次 ping 测试次数
MIN_SPEED = 5     # 最小下载速度（MB/s）
MAX_DELAY = 50    # 最大延迟（ms）
TIMEOUT = 1.5     # ping 超时时间（秒）
TEST_URL = "https://speed.cloudflare.com/__down?bytes=5000000"  # 5MB 测速文件

# Cloudflare IP 段（从 https://www.cloudflare.com/ips/ 获取）
CF_IP_RANGES = [
    "104.16.0.0/12", "172.64.0.0/13", "173.245.48.0/20", "103.21.244.0/22",
    "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
    "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17",
    "162.158.0.0/15", "104.24.0.0/14"
]

# ISP 优选地区
ISP_REGIONS = {
    "cu": ["Hong Kong", "Singapore", "Japan", "Taiwan"],  # 中国联通
    "cm": ["Hong Kong", "Taiwan", "South Korea", "Malaysia"],  # 中国移动
    "ct": ["Singapore", "Japan", "Malaysia", "Thailand"],  # 中国电信
    "cf": ["Hong Kong", "Singapore", "Japan", "Taiwan", "South Korea", "Malaysia", "Thailand"]  # 全网
}
