"""connections.py"""
import json
import logging
from typing import List, Dict, Tuple
import threading
import subprocess
import requests
from server_management.utils.models import Server

def check_ssh(server: Server, timeout: int = 2) -> bool:
    """
    Check if a server is online by attempting to connect to it via SSH.

    Parameters:
    server (Server): A Server object.
    timeout (int): The maximum time to wait for the SSH connection (in seconds).

    Returns:
    bool: True if the server is online (connection successful), False otherwise.
    """
    try:
        ssh_command = [
            "ssh",
            '-o', 'StrictHostKeyChecking=no',
            "-i", server.key_path,
            "-p", str(server.port),
            f"{server.username}@{server.ip}",
            "exit",
        ]
        # Attempt to connect via SSH using subprocess
        result = subprocess.run(
            ssh_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False
        )
        # If the return code is 0, the connection was successful
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logging.info("SSH connection failed for %s:%s: CalledProcessError %s", server.ip, server.port, e)
        return False
    except subprocess.TimeoutExpired as e:
        logging.info("SSH connection timed out for %s:%s: TimeoutExpired %s", server.ip, server.port, e)
        return False
    except subprocess.SubprocessError as e:
        logging.info("SSH connection error for %s:%s: SubprocessError %s", server.ip, server.port, e)
        return False

def check_ssh_worker(server: Server, offline_hostnames: List[str]):
    """
    Thread worker function to check SSH connectivity for a server.

    Parameters:
    server (Server): A Server object.s
    results (dict): A shared dictionary to store the results.
    """
    if not check_ssh(server):
        offline_hostnames.append(server.hostname)

def ping_bcm_servers(servers: List[Server]) -> Dict[str, bool]:
    """
    Ping a list of servers to check if they are online via SSH.

    Parameters:
    servers (list): A list of servers.

    Returns:
    dict: A dictionary where the keys are server IP addresses and the values are True (online) or False (offline).
    """
    offline_hostnames = []
    threads = []

    for server in servers:
        thread = threading.Thread(target=check_ssh_worker, args=(server, offline_hostnames))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return offline_hostnames

def get_offline_vast_bcm_servers(vast_api_key) -> Tuple[List[str], List[str]]:
    """
    Ping a list of servers to check if they are online.

    Parameters:
    servers (list): A list of dictionaries, each containing 'ip' (str) and 'port' (int) keys.

    Returns:
    dict: A dictionary where the keys are server IP addresses and the values are True (online) or False (offline).
    """
    url = "https://console.vast.ai/api/v0/machines"

    headers = {
	  'Accept': 'application/json',
	  'Authorization': 'Bearer ' + vast_api_key
	}
    timeout_seconds = 10

    listed_bcm_hostnames = []
    offline_hostnames = []
    try:
        response = requests.request("GET", url, headers=headers, timeout=timeout_seconds)
        json_response = json.loads(response.text)
        offline_bcm_machines = [
            machine for machine in json_response['machines']
            if machine['mobo_name'] == "ROMED8" and machine['timeout'] > 60 and machine['listed']
        ]
        listed_bcm_machines = [
            machine for machine in json_response['machines']
            if machine['mobo_name'] == "ROMED8" and machine['listed']
        ]
        # Extract the hostnames from the offline_bcm_machines
        offline_hostnames = [machine['hostname'] for machine in offline_bcm_machines]
        listed_bcm_hostnames = [machine['hostname'] for machine in listed_bcm_machines]
    except requests.Timeout:
        print(f"The request to {url} timed out after {timeout_seconds} seconds.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return (listed_bcm_hostnames, offline_hostnames)
