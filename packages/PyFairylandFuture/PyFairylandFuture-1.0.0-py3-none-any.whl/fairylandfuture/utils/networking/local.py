# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-02 02:42:14 UTC+8
"""

from typing import Dict

import socket
import netifaces


class LocalNetworkUtils:

    @classmethod
    def ip_address(cls) -> Dict[str, str]:
        default_ip_addr = socket.gethostbyname(socket.gethostname())
        ip_dict = {"default": default_ip_addr}

        for interface in netifaces.interfaces():
            addr_list = netifaces.ifaddresses(interface)
            for type in addr_list:
                if type == netifaces.AF_INET:
                    for info in addr_list.get(type):
                        ip_dict.update({interface: info.get("addr")})
        return ip_dict

    @classmethod
    def default_ip_address(cls) -> str:
        return cls.ip_address().get("default")
