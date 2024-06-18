"""file.py"""
import logging
import os
import time
from typing import List, Tuple
from server_management.utils.models import Server

def get_last_reboot(server_mgmt_dir: str, minutes_since_last_reboot: float) -> bool:
    """
    Args:
        server_mgmt_dir (str): Directory for server management
        minutes_since_last_reboot (float): Minutes since last reboot

    Returns:
        bool: Returns true if recently rebooted
    """

    file_name = 'last_reboot'
    file_path = os.path.join(server_mgmt_dir, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return False

    # Read the timestamp from the file
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    try:
        file_timestamp = float(file_content)
    except ValueError as e:
        logging.error("The file %s does not contain a valid timestamp: %s", file_path, e)
        return False

    # Get the current time
    current_time = time.time()

    # Calculate the difference in minutes
    time_difference = (current_time - file_timestamp) / 60

    # Check if the time since last boot has been longer than minutes specified
    return time_difference <= minutes_since_last_reboot

def set_last_reboot(server_mgmt_dir: str):
    """
    Args:
        server_mgmt_dir (str): Directory for server management

    Returns:
        List[str]
    """
    file_name = 'last_reboot'
    file_path = os.path.join(server_mgmt_dir, file_name)

    # Get the current time
    current_time = time.time()

    # Create the file and write the current time
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(current_time))

def create_bcm_sel_list_logs(logs_for_bcm_servers: List[Tuple[Server, str]], server_mgmt_dir: str) -> bool:
    """
    Args:
        logs_for_bcm_servers (List[Tuple[Server, str]]): List of servers and their logs
        server_mgmt_dir (str): Directory for server management

    Returns:
        bool: True if logs are successfully created, False otherwise
    """
    try:
        # Get the current time
        current_time = int(time.time())

        # Set the crash reports directory
        crash_reports_dir = f'{server_mgmt_dir}crashes/'

        # Ensure the directory exists
        os.makedirs(crash_reports_dir, exist_ok=True)

        for server, logs in logs_for_bcm_servers:
            file_name = f'{current_time}-{server.hostname}_bcm_sel_list.log'
            file_path = os.path.join(crash_reports_dir, file_name)

            # Create the file and write the current time
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(logs)

        return True

    except OSError as e:
        logging.error("OS error occurred while creating crash reports directory or writing files: %s", e)

    return False
