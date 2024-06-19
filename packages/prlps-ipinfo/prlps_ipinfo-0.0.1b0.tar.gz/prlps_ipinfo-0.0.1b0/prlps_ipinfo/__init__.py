from .ipinfo import IpInfo
from asyncio import run


def sync_ipinfo(ip: str | None = None, proxy: str | None = None) -> dict:
    ip_info = IpInfo(ip, proxy)
    return run(ip_info.get_ip_info())

async def async_ipinfo(ip: str | None = None, proxy: str | None = None) -> dict:
    ip_info = IpInfo(ip, proxy)
    return await ip_info.get_ip_info()

