import os

import geoip2.database
from geoip2.errors import AddressNotFoundError


def get_country_from_ip(ip_address: str) -> str:
    abs_path = os.path.abspath('./libs/GeoLite2-Country.mmdb')
    reader = geoip2.database.Reader(abs_path)
    try:
        response = reader.country(ip_address)
        return response.country.name
    except AddressNotFoundError:
        return "Unknown"
