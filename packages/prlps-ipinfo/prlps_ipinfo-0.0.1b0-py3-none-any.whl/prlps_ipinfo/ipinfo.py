from asyncio import as_completed, gather, run
from contextlib import asynccontextmanager
from re import sub
from typing import Any
from httpx import AsyncClient
from httpx_socks import AsyncProxyTransport


get_ip_services = [
    {'url': 'https://ipv4-internet.yandex.net/api/v0/ip', 'json': False, 'json_key': None},
    {'url': 'https://ipinfo.io/ip', 'json': False, 'json_key': None},
    {'url': 'https://ipapi.co/ip', 'json': False, 'json_key': None},
    {'url': 'https://ip.seeip.org/jsonip', 'json': True, 'json_key': 'ip'},
    {'url': 'https://ip.seeip.org', 'json': False, 'json_key': None},
    {'url': 'https://icanhazip.com/', 'json': False, 'json_key': None},
    {'url': 'https://api.myip.com', 'json': True, 'json_key': 'ip'},
    {'url': 'https://jsonip.com', 'json': True, 'json_key': 'ip'},
    {'url': 'https://ifconfig.me/ip', 'json': False, 'json_key': None},
    {'url': 'https://httpbin.org/ip', 'json': True, 'json_key': 'origin'},
    {'url': 'https://api.bigdatacloud.net/data/client-ip', 'json': True, 'json_key': 'ipString'},
    {'url': 'https://api.ipify.org/', 'json': False, 'json_key': None},
    {'url': 'https://api64.ipify.org/?format=json', 'json': True, 'json_key': 'ip'},
    {'url': 'https://api.ipgeolocation.io/getip', 'json': True, 'json_key': 'ip'},
    {'url': 'https://api.ip.sb/ip', 'json': False, 'json_key': None},
    {'url': 'http://checkip.amazonaws.com', 'json': False, 'json_key': None},
    {'url': 'https://api.my-ip.io/v1/ip', 'json': False, 'json_key': None},
    {'url': 'https://ip.guide/frontend/api', 'json': True, 'json_key': ['ip_response', 'ip']},
    {'url': 'https://ifconfig.co/json', 'json': True, 'json_key': 'ip'},
    {'url': 'https://ipwho.is/', 'json': True, 'json_key': 'ip'},
    {'url': 'https://ipwhois.app/json/', 'json': True, 'json_key': 'ip'},
    {'url': 'https://api.ip.sb/geoip', 'json': True, 'json_key': 'ip'},
    {'url': 'https://api.my-ip.io/v2/ip.json', 'json': True, 'json_key': 'ip'},
    {'url': 'https://wtfismyip.com/json', 'json': True, 'json_key': 'YourFuckingIPAddress'},
    {'url': 'https://proxylist.geonode.com/api/ip', 'json': True, 'json_key': 'ipV4'},
]


class IpInfo:
    def __init__(self, ip: str | None = None, proxy: str | None = None) -> None:
        self.ip = ip
        self.ip_provided = True if ip else False
        self.proxy = proxy
        self.protocols = ['socks5://', 'socks4://', 'http://', 'https://']
        if self.proxy and not any(proxy.startswith(protocol) for protocol in self.protocols):
            raise ValueError(f'строка прокси должна начинаться с одного из следующих протоколов: {", ".join(self.protocols)}')

    @asynccontextmanager
    async def httpx_client(self) -> AsyncClient:
        transport = AsyncProxyTransport.from_url(self.proxy) if self.proxy else None
        async with AsyncClient(timeout=30, verify=False, transport=transport, follow_redirects=True) as client:
            yield client

    async def fetch_ip(self, client: AsyncClient, url: str, json: bool, json_key: str | list) -> str | None:
        json_key = json_key if isinstance(json_key, list) else [json_key]
        try:
            response = await client.get(url)
            response.raise_for_status()
            ip = self.get_nested(response.json(), json_key) if json and json_key else response.text.strip().strip('\'"')
            return ip.strip()
        except:
            return None

    async def get_ip(self, client: AsyncClient):
        tasks = [self.fetch_ip(client, service['url'], service['json'], service['json_key']) for service in get_ip_services]
        for task in as_completed(tasks):
            result_ip = await task
            if result_ip:
                return result_ip
        return None

    @staticmethod
    async def fetch_ip_info(client: AsyncClient, url: str) -> dict[str, Any]:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'{url}: {e}'}

    @staticmethod
    def get_nested(data, keys, default=None):
        try:
            for key in keys:
                data = data.get(key, {})
                if not isinstance(data, dict):
                    return data
        except:
            pass
        return default

    def process_ip_guide(self, data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip_response', {}).get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'provider_country_code': self.get_nested(data, ['ip_response', 'network', 'autonomous_system', 'country']) or self.get_nested(data, ['network_response', 'autonomous_system', 'country']) or self.get_nested(
                data, ['autonomous_system_response', 'country']
                ),
            'country': self.get_nested(data, ['ip_response', 'location', 'country']),
            'city': self.get_nested(data, ['ip_response', 'location', 'city']),
            'timezone': self.get_nested(data, ['ip_response', 'location', 'timezone']),
            'latitude': self.get_nested(data, ['ip_response', 'location', 'latitude']),
            'longitude': self.get_nested(data, ['ip_response', 'location', 'longitude']),
            'owner': self.get_nested(data, ['ip_response', 'network', 'autonomous_system', 'organization']) or self.get_nested(data, ['network_response', 'autonomous_system', 'organization']) or self.get_nested(
                data, ['autonomous_system_response', 'organization']
                ),
            'proprietor': self.get_nested(data, ['ip_response', 'network', 'autonomous_system', 'name']) or self.get_nested(data, ['network_response', 'autonomous_system', 'name']) or self.get_nested(
                data, ['autonomous_system_response', 'name']
                ),
            'asn': self.get_nested(data, ['ip_response', 'network', 'autonomous_system', 'asn']) or self.get_nested(data, ['network_response', 'autonomous_system', 'asn']) or self.get_nested(data, ['autonomous_system_response', 'asn']),
            'rir': self.get_nested(data, ['ip_response', 'network', 'autonomous_system', 'rir']) or self.get_nested(data, ['network_response', 'autonomous_system', 'rir']) or self.get_nested(data, ['autonomous_system_response', 'rir']),
            'cidr': data.get('ip_response', {}).get('network', {}).get('cidr') or data.get('network_response', {}).get('cidr'),
            'hosts_start': data.get('ip_response', {}).get('network', {}).get('hosts', {}).get('start') or data.get('network_response', {}).get('hosts', {}).get('start'),
            'hosts_end': data.get('ip_response', {}).get('network', {}).get('hosts', {}).get('end') or data.get('network_response', {}).get('hosts', {}).get('end'),
            'routes_v4': self.get_nested(data, ['autonomous_system_response', 'routes', 'v4']),
            'routes_v6': self.get_nested(data, ['autonomous_system_response', 'routes', 'v6']),
        }

    def process_api_bigdatacloud_net(self, data: dict[str, Any], ip: str) -> dict[str, Any]:
        if "error" in data:
            return {}
        return {
            'ip': ip,
            'continent': data.get('continent') or next((item['name'] for item in self.get_nested(data, ['localityInfo', 'informative'], []) if item.get('description') == 'continent'), None),
            'provider_country_code': data.get('countryCode') or self.get_nested(data, ['localityInfo', 'administrative', 'isoCode']),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'country': sub(r'\s*\(.*\)', '', data.get('countryName') or self.get_nested(data, ['localityInfo', 'administrative', 'name'], []) or self.get_nested(data, ['localityInfo', 'administrative', 'isoName'], '')),
            'district': next((item['name'] for item in self.get_nested(data, ['localityInfo', 'administrative'], '') if item.get('adminLevel') == 3), []),
            'region': data.get('principalSubdivision') or next((item['name'] for item in self.get_nested(data, ['localityInfo', 'administrative'], []) if item.get('adminLevel') == 4), []),
            'provider_region_code': data.get('principalSubdivisionCode') or next((item['isoCode'] for item in self.get_nested(data, ['localityInfo', 'administrative'], []) if item.get('adminLevel') == 4), []),
            'city': data.get('city') or next((item['name'] for item in self.get_nested(data, ['localityInfo', 'administrative']) if item.get('order') == 6), None),
            'locality': data.get('locality') or next((item['name'] for item in self.get_nested(data, ['localityInfo', 'administrative'], []) if item.get('order') == 8), None),
            'timezone': next((item['name'] for item in self.get_nested(data, ['localityInfo', 'informative'], []) if item.get('description') == 'time zone'), None)
        }

    def process_ipinfo_io(self, data: dict[str, Any], ip: str) -> dict[str, Any]:
        if "error" in data:
            return {}
        data = data.get('data')
        is_mobile = True if self.get_nested(data, ['carrier', 'mcc']) else False
        return {
            'ip': ip,
            'is_hosting_or_vpn': self.get_nested(data, ['privacy', 'hosting']) or self.get_nested(data, ['privacy', 'vpn']) or self.get_nested(data, ['privacy', 'proxy']) or self.get_nested(data, ['privacy', 'tor']) or self.get_nested(
                data, ['privacy', 'relay']
                ),
            'host': data.get('hostname'),
            'latitude': float(data.get('loc', ',').split(',')[0]),
            'longitude': float(data.get('loc', ',').split(',')[1]),
            'city': data.get('city'),
            'postal_code': data.get('postal'),
            'region': data.get('region'),
            'provider_country_code': data.get('country'),
            'timezone': data.get('timezone'),
            'owner': self.get_nested(data, ['asn', 'name']),
            'proprietor': self.get_nested(data, ['company', 'name']),
            'asn': self.get_nested(data, ['asn', 'asn']),
            'is_mobile': is_mobile,
            'operator': self.get_nested(data, ['carrier', 'name']) or data.get('org'),
        }

    @staticmethod
    def process_ipapi_co(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'country': data.get('country_name'),
            'provider_country_code': data.get('country'),
            'region': data.get('region'),
            'city': data.get('city'),
            'provider_region_code': data.get('region_code'),
            'timezone': data.get('timezone'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'utc_offset': (offset := data.get('utc_offset'))[:3] + ':' + offset[3:],
            'owner': data.get('org'),
            'asn': data.get('asn'),
        }

    def process_ifconfig_co(self, data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'country': data.get('country'),
            'provider_country_code': data.get('country_iso'),
            'region': data.get('region_name'),
            'city': data.get('city'),
            'provider_region_code': data.get('region_code'),
            'timezone': data.get('time_zone'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'owner': data.get('asn_org'),
            'asn': data.get('asn'),
            'user_agent': self.get_nested(data, ['user_agent', 'raw_value']),
        }

    def process_ipinfo_info(self, data: dict[str, Any], ip: str) -> dict[str, Any]:
        if "error" in data:
            return {}
        is_crawler = self.get_nested(data, ['security', 'crawler_name']) + ' (' + self.get_nested(data, ['security', 'crawler_type']) + ')' if self.get_nested(data, ['security', 'is_crawler']) else False
        utc_offset = self.get_nested(data, ['time_zone', 'gmt_offset'])
        utc_offset = utc_offset if utc_offset else 0

        return {
            'ip': ip,
            'continent': data.get('continent_name'),
            'country': data.get('country_name'),
            'provider_country_code': data.get('country_code'),
            'provider_region_code': data.get('region_code'),
            'region': data.get('region_name'),
            'city': data.get('city'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': self.get_nested(data, ['time_zone', 'id']),
            'utc_offset': f'{"-" if utc_offset < 0 else "+"}{int(divmod(abs(utc_offset), 3600)[0]):02}:{int(divmod(abs(utc_offset), 3600)[1] // 60):02}',
            'owner': self.get_nested(data, ['connection', 'isp']),
            'asn': self.get_nested(data, ['connection', 'asn']),
            'is_crawler': is_crawler,
        }

    @staticmethod
    def process_api_bigdatacloud_net_client(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ipString', '')
        return {'ip' if ':' not in ip else 'ipv6': ip, 'user_agent': data.get('userAgentRaw'), }

    def process_ipwho_is(self, data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'continent': data.get('continent'),
            'country': data.get('country'),
            'region': data.get('region'),
            'city': data.get('city'),
            'provider_country_code': data.get('country_code'),
            'provider_region_code': data.get('region_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': (self.get_nested(data, ['timezone', 'id']) or '').replace('\\/', '/'),
            'utc_offset': self.get_nested(data, ['timezone', 'utc']),
        }

    @staticmethod
    def process_ipwhois_app(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'continent': data.get('continent'),
            'country': data.get('country'),
            'region': data.get('region'),
            'city': data.get('city'),
            'provider_country_code': data.get('country_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone'),
            'utc_offset': data.get('timezone_gmt'),
            'asn': data.get('asn'),
        }

    @staticmethod
    def process_api_ip_sb_geoip(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        utc_offset = data.get('offset')
        utc_offset = utc_offset if utc_offset else 0
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'country': data.get('country'),
            'region': data.get('region'),
            'city': data.get('city'),
            'provider_country_code': data.get('country_code'),
            'provider_region_code': data.get('region_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone'),
            'utc_offset': f'{"-" if utc_offset < 0 else "+"}{int(divmod(abs(utc_offset), 3600)[0]):02}:{int(divmod(abs(utc_offset), 3600)[1] // 60):02}',
            'asn': data.get('asn'),
        }

    def process_api_my_ip_io(self, data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        ip = data.get('ip', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'country': self.get_nested(data, ['country', 'name']),
            'region': data.get('region'),
            'city': data.get('city'),
            'provider_country_code': self.get_nested(data, ['country', 'code']),
            'latitude': self.get_nested(data, ['location', 'lat']),
            'longitude': self.get_nested(data, ['location', 'lon']),
            'timezone': data.get('timeZone'),
            'owner': self.get_nested(data, ['asn', 'name']),
            'asn': self.get_nested(data, ['asn', 'number']),
        }

    @staticmethod
    def process_wtfismyip_com(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}

        def _get(key):
            return data.get('YourFucking' + key)

        ip = data.get('IPAddress', '')
        return {
            'ip' if ':' not in ip else 'ipv6': ip,
            'country': _get('Country'),
            'city': _get('City'),
            'provider_country_code': _get('CountryCode'),
            'provider_region_code': (_get('Location') or '').split(',')[1].strip(),
            'owner': _get('ISP'),
        }

    @staticmethod
    def proxylist_geonode_com_api_ip(data: dict[str, Any]) -> dict[str, Any]:
        if "error" in data:
            return {}
        data = data.get('data')
        utc_offset = data.get('offset')
        utc_offset = utc_offset if utc_offset else 0
        return {
            'ip': data.get('ipV4') if not data.get('ipV6') else '',
            'continent': data.get('continent'),
            'country': data.get('country'),
            'city': data.get('city'),
            'provider_country_code': data.get('iso2'),
            'provider_region_code': data.get('region'),
            'region': data.get('regionName'),
            'latitude': data.get('lat'),
            'longitude': data.get('lon'),
            'timezone': data.get('timezone'),
            'utc_offset': f'{"-" if utc_offset < 0 else "+"}{int(divmod(abs(utc_offset), 3600)[0]):02}:{int(divmod(abs(utc_offset), 3600)[1] // 60):02}',
            'is_hosting_or_vpn': data.get('hosting'),
            'is_mobile': data.get('mobile'),
            'operator': data.get('org') or data.get('asname'),
            'asn': data.get('as', '').split(' ')[0][2:],
            'ipv6': data.get('ipV6'),
            'owner': data.get('isp'),
        }

    @staticmethod
    def merge_results(results: list[dict[str, Any]]) -> dict[str, Any]:
        merged_data = {}
        preference_order = {
            'ip': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'ipv6': [13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'provider_country_code': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'provider_region_code': [4, 5, 6, 8, 10, 12, 1],
            'continent': [6, 1, 8, 9],
            'country': [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'district': [2],
            'region': [1, 3, 4, 5, 8, 9, 10, 11, 6],
            'city': [3, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'locality': [2],
            'timezone': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'utc_offset': [1, 6, 8, 9, 10],
            'latitude': [3, 6, 1, 4, 5, 10, 11, 8, 9, 2],
            'longitude': [3, 6, 1, 4, 5, 10, 11, 8, 9, 2],
            'owner': [1, 3, 4, 5, 6, 11, 12],
            'proprietor': [1, 3],
            'asn': [3, 4, 5, 9, 1, 6, 10, 11],
        }
        for key, order in preference_order.items():
            for idx in order:
                idx = idx - 1
                if key in results[idx]:
                    merged_data[key] = results[idx][key]
                    break
            else:
                for result in results:
                    if key in result:
                        merged_data[key] = result[key]
                        break
        for result in results:
            for key, value in result.items():
                if key not in merged_data and value is not None:
                    merged_data[key] = value
        return merged_data

    async def get_ip_info(self) -> dict[str, Any]:
        async def dummy(): return {}
        async with self.httpx_client() as client:
            if not self.ip:
                self.ip = await self.get_ip(client)
            tasks = [
                self.fetch_ip_info(client, 'https://ip.guide/frontend/api') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://api.bigdatacloud.net/data/reverse-geocode-client') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, f'https://ipinfo.io/widget/demo/{self.ip}'),
                self.fetch_ip_info(client, 'https://ipapi.co/json') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://ifconfig.co/json') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, f'https://ipinfo.info/ip_api.php?ip={self.ip}'),
                self.fetch_ip_info(client, 'https://api.bigdatacloud.net/data/client-info') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://ipwho.is/') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://ipwhois.app/json/') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://api.ip.sb/geoip') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://api.my-ip.io/v2/ip.json') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://wtfismyip.com/json') if not self.ip_provided else dummy(),
                self.fetch_ip_info(client, 'https://proxylist.geonode.com/api/ip') if not self.ip_provided else dummy(),
            ]
            results = await gather(*tasks)

        processed_results = [
            self.process_ip_guide(results[0]) if not self.ip_provided else {},
            self.process_api_bigdatacloud_net(results[1], self.ip) if not self.ip_provided else {},
            self.process_ipinfo_io(results[2], self.ip),
            self.process_ipapi_co(results[3]) if not self.ip_provided else {},
            self.process_ifconfig_co(results[4]) if not self.ip_provided else {},
            self.process_ipinfo_info(results[5], self.ip),
            self.process_api_bigdatacloud_net_client(results[6]) if not self.ip_provided else {},
            self.process_ipwho_is(results[7]) if not self.ip_provided else {},
            self.process_ipwhois_app(results[8]) if not self.ip_provided else {},
            self.process_api_ip_sb_geoip(results[9]) if not self.ip_provided else {},
            self.process_api_my_ip_io(results[10]) if not self.ip_provided else {},
            self.process_wtfismyip_com(results[11]) if not self.ip_provided else {},
            self.proxylist_geonode_com_api_ip(results[12]) if not self.ip_provided else {},
        ]

        return self.merge_results(processed_results)


