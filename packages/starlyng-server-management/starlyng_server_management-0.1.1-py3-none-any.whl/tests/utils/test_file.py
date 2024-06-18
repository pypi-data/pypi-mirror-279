"""
Testing for file module
"""
import os
import time
import pytest
from server_management.utils.file import get_last_reboot, set_last_reboot, create_bcm_sel_list_logs
from server_management.utils.models import Server

@pytest.fixture
def tmp_server_mgmt_dir(tmpdir):
    """Fixture to create a temporary directory for server management."""
    return tmpdir.mkdir("server_mgmt")

def test_get_last_reboot_no_file(tmp_server_mgmt_dir):
    """Test when the last reboot file does not exist."""
    assert not get_last_reboot(str(tmp_server_mgmt_dir), 5)

def test_get_last_reboot_invalid_timestamp(tmp_server_mgmt_dir, caplog):
    """Test when the last reboot file contains invalid timestamp."""
    file_path = tmp_server_mgmt_dir.join('last_reboot')
    file_path.write("invalid_timestamp")

    assert not get_last_reboot(str(tmp_server_mgmt_dir), 5)
    assert "does not contain a valid timestamp" in caplog.text

def test_get_last_reboot_recent_reboot(tmp_server_mgmt_dir):
    """Test when the last reboot was recent."""
    current_time = time.time()
    file_path = tmp_server_mgmt_dir.join('last_reboot')
    file_path.write(str(current_time))

    assert get_last_reboot(str(tmp_server_mgmt_dir), 5)

def test_get_last_reboot_not_recent_reboot(tmp_server_mgmt_dir):
    """Test when the last reboot was not recent."""
    current_time = time.time() - 10 * 60  # 10 minutes ago
    file_path = tmp_server_mgmt_dir.join('last_reboot')
    file_path.write(str(current_time))

    assert not get_last_reboot(str(tmp_server_mgmt_dir), 5)

def test_set_last_reboot(tmp_server_mgmt_dir):
    """Test setting the last reboot timestamp."""
    set_last_reboot(str(tmp_server_mgmt_dir))
    file_path = tmp_server_mgmt_dir.join('last_reboot')

    assert file_path.check(file=1)
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        file_timestamp = float(file_content)
        assert abs(file_timestamp - time.time()) < 1  # Timestamp should be within 1 second

def test_create_bcm_sel_list_logs(tmp_server_mgmt_dir):
    """Test creating BCM SEL list logs."""
    server_mgmt_dir = str(tmp_server_mgmt_dir) + '/'
    starlyng01 = Server('starlyng01', '192.168.0.11', '/path/to/key', '22', 'testuser', 'testbcmuser', 'testbcmpass', '234')
    logs_for_bcm_servers = [(starlyng01, "test log content")]
    assert create_bcm_sel_list_logs(logs_for_bcm_servers, server_mgmt_dir)

    crash_reports_dir = os.path.join(server_mgmt_dir, 'crashes')
    print(f"Checking if directory exists: {crash_reports_dir}")
    print(f"Contents of server_mgmt_dir: {os.listdir(server_mgmt_dir)}")

    assert os.path.exists(crash_reports_dir)
    assert len(os.listdir(crash_reports_dir)) == 1

    log_file = os.listdir(crash_reports_dir)[0]
    with open(os.path.join(crash_reports_dir, log_file), 'r', encoding='utf-8') as f:
        assert f.read() == "test log content"

def test_create_bcm_sel_list_logs_os_error(tmp_server_mgmt_dir, monkeypatch):
    """Test creating BCM SEL list logs with OSError."""
    server_mgmt_dir = str(tmp_server_mgmt_dir) + '/'
    starlyng01 = Server('starlyng01', '192.168.0.11', '/path/to/key', '22', 'testuser', 'testbcmuser', 'testbcmpass', '234')
    logs_for_bcm_servers = [(starlyng01, "test log content")]

    def mock_makedirs_fail(*args, **kwargs):
        raise OSError("Mocked OS error")

    monkeypatch.setattr(os, 'makedirs', mock_makedirs_fail)
    assert not create_bcm_sel_list_logs(logs_for_bcm_servers, server_mgmt_dir)
