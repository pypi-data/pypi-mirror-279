"""models.py"""
from dataclasses import dataclass

@dataclass
class Server:
    # pylint: disable=too-many-instance-attributes
    """
    Represents a server with an IP address, port, and hostname.

    Attributes:
        hostname (str): The hostname of the server.
        ip (str): The IP address of the server.
        key_path (str): The key path of the server.
        port (str): The port number of the server.
        username (str): The username that you want to log into on the server.
        bcm_user (str): The username that you want to log into via bcm.
        bcm_pass (str): The password that you want to log into via bcm.
        bcm_port (str): The bcm port number of the server.
    """
    hostname: str
    ip: str
    key_path: str
    port: str
    username: str
    bcm_user: str
    bcm_pass: str
    bcm_port: str
