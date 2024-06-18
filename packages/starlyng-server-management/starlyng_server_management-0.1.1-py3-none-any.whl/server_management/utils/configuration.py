"""configuration.py"""
from pathlib import Path
import argparse
import os
import logging
from typing import List
from dotenv import load_dotenv
from server_management.utils.models import Server
from server_management.utils.conversion import get_bcm_port, get_hostname

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run server management scripts.")
    parser.add_argument('--bcm_servers', type=str, help="Comma-separated list of bcm servers in the format ip:port.")
    parser.add_argument('--bcm_user', type=str, help="BCM username.")
    parser.add_argument('--bcm_pass', type=str, help="BCM password.")
    parser.add_argument('--ssh_key_path', type=str, help="Path to the SSH key.")
    parser.add_argument('--ssh_username', type=str, help="SSH username.")
    parser.add_argument('--vast_api_key', type=str, help="Vast API key.")
    parser.add_argument('--server_mgmt_dir', type=str, help="Server management directory.")
    return parser.parse_args()

def load_env_variables(dotenv_path=None):
    """Load environment variables from a .env file if it exists."""
    try:
        if dotenv_path is None:
            logging.info("No dotenv_path provided, skipping loading environment variables.")
            return

        if not Path(dotenv_path).exists():
            raise FileNotFoundError(f"The specified dotenv file does not exist: {dotenv_path}")

        load_dotenv(dotenv_path=dotenv_path)
    except (FileNotFoundError, PermissionError, OSError, TypeError) as error:
        logging.error("An error occurred: %s", error)

def get_configuration(args):
    """Retrieve configuration details, prioritizing command-line arguments, then environment variables."""

    bcm_servers_str = args.bcm_servers or os.getenv('BCM_SERVERS')
    bcm_user_str = args.bcm_user or os.getenv('BCM_USER')
    bcm_pass_str = args.bcm_pass or os.getenv('BCM_PASS')
    ssh_key_path_str = args.ssh_key_path or os.getenv('SSH_KEY_PATH')
    ssh_username_str = args.ssh_username or os.getenv('SSH_USERNAME')
    vast_api_key_str = args.vast_api_key or os.getenv('VAST_API_KEY')
    server_mgmt_dir_str = args.server_mgmt_dir or os.getenv('SERVER_MGMT_DIR')

    required_fields = [
        bcm_servers_str,
        bcm_user_str,
        bcm_pass_str,
        ssh_key_path_str,
        ssh_username_str,
        vast_api_key_str,
        server_mgmt_dir_str,
    ]

    if any(not field for field in required_fields):
        raise ValueError(
            "Missing configuration: ensure servers, bcm_pass, bcm_pass, ssh_key_path, "
            "ssh_username, vast_api_key, and server_mgmt_dir_str are provided."
        )

    bcm_servers = [tuple(server.split(':')) for server in bcm_servers_str.split(',')]
    bcm_servers = [(ip, int(port)) for ip, port in bcm_servers]
    formatted_servers: List[Server] = []
    for server_ip, server_port in bcm_servers:
        server_info = {
            'hostname': get_hostname(server_ip, server_port),
            'ip': server_ip,
            'key_path': ssh_key_path_str,
            'port': server_port,
            'username': ssh_username_str,
            'bcm_user': bcm_user_str,
            'bcm_pass': bcm_pass_str,
            'bcm_port': get_bcm_port(server_ip, server_port),
        }
        formatted_servers.append(Server(**server_info))

    return formatted_servers, vast_api_key_str, server_mgmt_dir_str

def load_configuration(dotenv_path=None):
    """
    Loads configuration from command-line arguments, environment variables, and .env file if it exists.

    This function first attempts to load the server configuration, SSH key path, and username
    from command-line arguments. If they are not provided, it falls back to environment variables 
    or the .env file located in the current working directory or a provided path.

    Returns:
        tuple: A tuple containing:
            - bcm_servers (list of tuples): A list of bcm servers.
            - vast_api_key (str): Vast API key.
    """
    args = parse_arguments()
    load_env_variables(dotenv_path=dotenv_path)
    return get_configuration(args)
