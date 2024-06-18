from typing import Optional
from dataclasses import dataclass


@dataclass
class SDKProxy:
    proxy_username: str = ""
    proxy_password: str = ""
    proxy_host: Optional[str] = None
    proxy_port: Optional[int] = None
    proxy_domain: str = ""


    def __str__(self):
        return (
            f"Proxy Username: {self.proxy_username}, "
            f"Proxy Password: {self.proxy_password}, "
            f"Proxy Host: {self.proxy_host}, "
            f"Proxy Port: {self.proxy_port}, "
            f"Proxy Domain: {self.proxy_domain}"
        )
