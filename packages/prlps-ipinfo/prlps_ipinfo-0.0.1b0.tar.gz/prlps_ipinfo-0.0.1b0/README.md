### че это
получение подробной информации о ip.

поддерживает прокси: socks5/4, https(s).

асинхронный и синхронный вариант.

### как использовать:

сначала установить:  `pip install prlps_ipinfo`

пример использования:

```python
# асинхронный вариант:
from prlps_ipinfo import async_ipinfo

async def your_async_func():
    my_ip = await async_ipinfo()  # информация о текущем ip соединения
    print(my_ip)
    proxy_ip = await async_ipinfo(proxy='socks5://prolaps.io:13115')  # информация о ip через прокси
    print(proxy_ip)
    someone_ip = await async_ipinfo(ip='34.106.124.244')  # информация о чужом ip
    print(someone_ip)


# асинхронный вариант с созданием экземпляра класса:
from prlps_ipinfo import IpInfo

async def your_another_async_func():
    my_ip_info = IpInfo()
    print(my_ip_info.get_ip_info())
    print(my_ip_info.ip)
    
    proxy_ip_info = IpInfo(proxy='http://127.0.0.1:8080')
    print(proxy_ip_info.get_ip_info())
    print(proxy_ip_info.ip)
    
    someone_ip_info = IpInfo(ip='34.106.124.244')
    print(someone_ip_info.get_ip_info())
    print(someone_ip_info.ip)


# синхронный вариант:
from prlps_ipinfo import sync_ipinfo

my_ip = sync_ipinfo()  # информация о текущем ip соединения
print(my_ip)
proxy_ip = sync_ipinfo(proxy='socks5://prolaps.io:13115')  # информация о ip через прокси
print(proxy_ip)
someone_ip = sync_ipinfo(ip='34.106.124.244')  # информация о чужом ip
print(someone_ip)
```

играйся 😊
