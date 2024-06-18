"""execute.py"""
from typing import List
from server_management.utils.bcm import (
    check_bcm_chassis_power_status,
    power_off_bcm_servers,
    power_on_bcm_servers,
    sel_list_bcm_servers,
    sel_clear_bcm_servers
)
from server_management.utils.file import set_last_reboot, create_bcm_sel_list_logs
from server_management.utils.models import Server
from server_management.utils.connections import ping_bcm_servers, get_offline_vast_bcm_servers

def execute_get_offline_hostnames(bcm_servers: List[Server], vast_api_key: str) -> List[Server]:
    """
    Args:
        bcm_servers (List[Server]): A list of servers.
        vast_api_key (List[str]): Vast API key.

    Returns:
        List[str]
    """
    offline_bcm_server_ping_hostnames = ping_bcm_servers(bcm_servers)
    offline_vast_bcm_servers = get_offline_vast_bcm_servers(vast_api_key)
    listed_hostnames = offline_vast_bcm_servers[0]
    offline_vast_bcm_server_offline_status_hostnames = offline_vast_bcm_servers[1]
    offline_hostnames = list(set(offline_bcm_server_ping_hostnames + offline_vast_bcm_server_offline_status_hostnames))
    # listed_offline_hostnames will make sure we're only rebooting listed machines that went offline.
    listed_offline_hostnames = [item for item in offline_hostnames if item in listed_hostnames]

    return [server for server in bcm_servers if server.hostname in listed_offline_hostnames]

def execute_smart_reboot_for_offline_hostnames(offline_bcm_servers: List[Server], server_mgmt_dir: str):
    """
    Args:
        offline_bcm_servers (List[str]): A list of offline servers.

    Returns:
        None
    """
    # Set time of last reboot
    set_last_reboot(server_mgmt_dir)
    bcm_server_offline_chassis_power_status = check_bcm_chassis_power_status(offline_bcm_servers)
    active_offline_servers = [item[0] for item in bcm_server_offline_chassis_power_status if item[1] == "Chassis Power is on"]
    # Only power off servers that are on
    power_off_bcm_servers(active_offline_servers)
    power_on_bcm_servers(offline_bcm_servers)
    # Log errors
    logs_for_bcm_servers = sel_list_bcm_servers(offline_bcm_servers)
    create_bcm_sel_list_logs(logs_for_bcm_servers, server_mgmt_dir)
    # Clear logs from crashed machines to clean up future crash logs
    sel_clear_bcm_servers(offline_bcm_servers)
