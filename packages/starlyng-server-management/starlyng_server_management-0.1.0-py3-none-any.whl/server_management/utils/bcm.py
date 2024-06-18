"""bcm.py"""
import logging
import subprocess
import threading
from typing import List, Tuple
from server_management.utils.models import Server

def bcm_command(server: Server, command: str) -> List[str]:
    """ Returns an ssh command that can be passed to subprocess.run

    Args:
        server (Server):
        command (str):

    Returns:
        List[str]:
    """
    base_command = [
        "ipmitool",
        "-I", "lanplus",
        "-H", server.ip,
        "-U", server.bcm_user,
        "-P", server.bcm_pass,
        "-p", server.bcm_port,
    ]
    # Split the command string by spaces and extend the base command
    return base_command + command.split()

def run_bcm_subprocess(server: Server, command: str, subprocess_result: List[Tuple[Server, str]]=None) -> subprocess.CompletedProcess:
    """
    Executes a command on a remote server via SSH and logs any errors.

    Args:
        server (Any): An instance containing the server's connection details.
        command (str): The command to execute on the remote server.
        subprocess_result (List[Tuple[Server, str]]): Result from the subprocess.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess run, containing information about the executed command.

    Logs:
        Logs errors if the command execution fails or if there is any error output from the command.
    """
    try:
        result = subprocess.run(bcm_command(server, command), capture_output=True, text=True, check=False)
        if subprocess_result is not None:
            subprocess_result.append((server, result.stdout.strip()))
        if result.stderr:
            logging.error("run_subprocess: Errors from %s:%s %s\n%s", server.ip, server.bcm_port, command, result.stderr)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.bcm_port, e)
        result = subprocess.CompletedProcess(args=command, returncode=e.returncode, stdout='', stderr=str(e))
    return result

def bcm_threaded_process(servers: List[Server], command: str, result: List[Tuple[Server, str]]=None):
    """
    Parameters:
    servers (list): A list of servers.
    command (str): A list of servers.
    result (List[Tuple[Server, str]]): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    threads = []

    for server in servers:
        thread = threading.Thread(target=run_bcm_subprocess, args=(server, command, result))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def check_bcm_chassis_power_status(servers: List[Server]) -> List[Tuple[Server, str]]:
    """
    Parameters:
    servers (list): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    chassis_power_status = []
    bcm_threaded_process(servers, "chassis power status", chassis_power_status)
    return chassis_power_status

def power_off_bcm_servers(servers: List[Server]) -> List[Tuple[Server, str]]:
    """
    Parameters:
    servers (list): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    chassis_power_off = []
    bcm_threaded_process(servers, "chassis power off", chassis_power_off)
    return chassis_power_off

def power_on_bcm_servers(servers: List[Server]) -> List[Tuple[Server, str]]:
    """
    Parameters:
    servers (list): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    chassis_power_on = []
    bcm_threaded_process(servers, "chassis power on", chassis_power_on)
    return chassis_power_on


def sel_list_bcm_servers(servers: List[Server]) -> List[Tuple[Server, str]]:
    """
    Parameters:
    servers (list): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    sel_list = []
    bcm_threaded_process(servers, "sel list", sel_list)
    return sel_list

def sel_clear_bcm_servers(servers: List[Server]) -> List[Tuple[Server, str]]:
    """
    Parameters:
    servers (list): A list of servers.

    Returns:
    List[Tuple[Server, str]]: A list of servers and the result.
    """
    sel_clear = []
    bcm_threaded_process(servers, "sel clear", sel_clear)
    return sel_clear
