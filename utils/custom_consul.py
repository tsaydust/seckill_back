import socket
from typing import Tuple
import consul
import uuid
from .single import SingletonMeta


def get_ip_port() -> Tuple[str, int]:
    sock_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_ip.connect(("8.8.8.8", 80))
    ip = sock_ip.getsockname()[0]
    sock_ip.close()
    sock_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_port.bind(("", 0))
    _, port = sock_port.getsockname()
    sock_port.close()
    return ip, port


class CustomConsul(metaclass=SingletonMeta):
    def __init__(self):
        self.service_id = uuid.uuid4().hex
        self.client = consul.Consul(host="localhost", port=8500)
        self.ip, self.port = get_ip_port()

    def register(self):
        self.client.agent.service.register(
            name="user_service",
            service_id=self.service_id,
            address=self.ip,
            port=self.port,
            tags=['user', 'grpc'],
            check=consul.Check.tcp(host=self.ip, port=self.port, interval='10s')
        )

    def deregister(self):
        self.client.agent.service.deregister(service_id=self.service_id)

    def get_port(self):
        return self.port

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.deregister()
