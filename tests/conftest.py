import pytest
from src.remote_connection import RemoteConnection


@pytest.fixture(scope="module")
def remote_conn():
    conn = RemoteConnection("172.23.36.12", "root", "TiaspftVix")
    conn.open_connection()

    marker = "without NTP"
    log_path = "/var/opt/htm/log"
    log_name = "DeviceServiceMonitor.log"

    # Crash detection before running tests
    if conn.is_service_crashing(log_path, log_name, marker):
        conn.close_connection()
        pytest.fail("Aborting tests: Service is restarting repeatedly (possible crash).", pytrace=False)

    # Ensure the marker is present in the log
    line_number = conn.get_latest_service_start_line(log_path, log_name, marker)
    if line_number is None or line_number <= 0:
        conn.close_connection()
        pytest.fail(f"Aborting tests: Restart marker '{marker}' not found in log.", pytrace=False)

    # Start log streaming from that point
    conn.start_log_stream_from_latest_restart(log_path, log_name, marker)

    yield conn

    conn.close_connection()
