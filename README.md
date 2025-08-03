# Cloudflare 优选 IP 项目

这是一个基于 Python 的工具，用于优化 Cloudflare DNS 记录，通过筛选低延迟、高速度的 IP 提升访问速度，支持三网分流（中国电信、中国移动、中国联通）和全球访问。

## 功能
- **优选 IP 筛选**：测试 Cloudflare IP，筛选延迟 <50ms、速度 >5MB/s 的 IP。
- **三网分流**：为中国电信 (`ct`)、中国移动 (`cm`)、中国联通 (`cu`) 和全球 (`cf`) 配置专用 IP。
- **异步多线程**：使用 `aiohttp` 和 `pythonping` 进行高效测速。
- **CDN 加速**：启用 Cloudflare 代理，加速全球访问。
- **自动化 DNS 更新**：通过 Cloudflare API 更新 DNS 记录，支持重试机制。
- **CI/CD 集成**：使用 GitHub Actions 自动检查代码、运行测试和部署。

## 前提条件
- Python 3.8+
- Cloudflare API Token（需要 `Zone:Edit` 和 `DNS:Edit` 权限）
- Cloudflare 管理的域名

## 安装
1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/cloudflare-optimizer.git
   cd cloudflare-optimizer# ips
