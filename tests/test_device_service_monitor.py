import time
from pytest import mark


@mark.dsm
class TestDeviceServiceMonitor:
    @mark.smoke
    def test_device_service_monitor_started_without_ntp(self, remote_conn):
        time.sleep(5)  # Give some time for logs to be collected

        assert remote_conn.validate_in_logs("without NTP"), \
            "DeviceServiceMonitor started without NTP "

    @mark.smoke
    def test_device_service_monitor_initialized_ignition_monitor(self, remote_conn):
        time.sleep(5)  # Give some time for logs to be collected

        assert remote_conn.validate_in_logs("Trying to initialize ignition monitor..."), \
            "DSM starting initialization of ignition monitor."
        assert remote_conn.validate_in_logs("Ignition monitor initialized successfully."), \
            "DSM initialized ignition monitor successfully."
        assert remote_conn.validate_in_logs("Ignition State is 1"), \
            "DSM Ignition State is 1 "

    @mark.smoke
    def test_device_service_monitor_started_acquired_current_time(self, remote_conn):
        time.sleep(5)  # Give some time for logs to be collected

        assert remote_conn.validate_in_logs("DSM working on NTP Sync."), \
            "DSM started working on NTP Sync."
        assert remote_conn.validate_in_logs("Attempting to retrieve ntp date"), \
            "DSM Attempting to retrieve ntp date."
        assert remote_conn.validate_in_logs("Got date information"), \
            "DSM Got date information from ntp server."
        assert remote_conn.validate_in_logs("Time is set to"), \
            "DSM setting up the device time to current time."

    @mark.smoke
    def test_device_service_monitor_started_with_ntp(self, remote_conn):
        time.sleep(5)  # Give some time for logs to be collected

        assert remote_conn.validate_in_logs("====================== Starting DeviceServiceMonitor "), \
            "DeviceServiceMonitor started with NTP "

    @mark.smoke
    def test_device_service_monitor_initializing_leaderfollower_selection(self, remote_conn):
        time.sleep(5)  # Give some time for logs to be collected

        assert remote_conn.validate_in_logs("DSM working on Leader/Follower initialization.."), \
            "DSM started working on Leader/Follower initialization.  "

        assert remote_conn.validate_in_logs("Trying to initialize LeaderFollower..."), \
            "DSM trying to initialize LeaderFollower selection logic. "

    # @mark.smoke
    # def test_device_service_monitor_device_role_assigned(self, remote_conn):
    #     assert remote_conn.validate_in_logs("Current role has changed"), \
    #         "DSM changed the current role of device."
    #
    #     assert remote_conn.validate_in_logs("LeaderFollower initialized successfully. Current role:"), \
    #         "DSM  initialized LeaderFollower selection logic successfully."

    @mark.smoke
    def test_device_service_monitor_device_role_assigned(self, remote_conn):
        assert remote_conn.validate_in_logs("Current role has changed"), \
            "DSM changed the current role of device."

        log1 = 'LeaderFollower initialized successfully. Current role: Leader'
        log2 = 'LeaderFollower initialized successfully. Current role: Follower'

        assert remote_conn.validate_in_logs(log1) or remote_conn.validate_in_logs(log2), \
            "DSM did not log the expected role assignment (Leader or Follower)."

    def test_device_service_monitor_application_management_started(self, remote_conn):
        assert remote_conn.validate_in_logs("DSM working on Application Management.."), \
            "DSM started working on Application Management."

    def test_device_service_monitor_started_ntp_client(self, remote_conn):
        assert remote_conn.validate_in_logs("Triggering NTP command = /afc/bin/ntpclient -t -s -l -h "), \
            "DSM triggered NTP command."
        assert remote_conn.validate_in_logs("[ntpclient] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "NTP client app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[ntpclient] Starting application ..."), \
            "DSM starting NTP client."
        assert remote_conn.validate_in_logs("[ntpclient] Application started"), \
            "DSM started NTP client with a PID."

    def test_device_service_monitor_started_user_interface(self, remote_conn):
        assert remote_conn.validate_in_logs("[UserInterface] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "User Interface app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[UserInterface] Starting application ..."), \
            "DSM starting User Interface."
        assert remote_conn.validate_in_logs("[UserInterface] Application started"), \
            "DSM started User Interface with a PID."
        assert remote_conn.validate_in_logs("[UserInterface] Modifying app state from AboutToBeStarted -> Running"), \
            "User Interface app state changed to 'Running' from 'AboutToBeStarted'"

    def test_device_service_monitor_started_validator(self, remote_conn):
        assert remote_conn.validate_in_logs("[Validator] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "Validator app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[Validator] Starting application ..."), \
            "DSM starting Validator."
        assert remote_conn.validate_in_logs("[Validator] Application started"), \
            "DSM started Validator with a PID."
        assert remote_conn.validate_in_logs("[Validator] Modifying app state from AboutToBeStarted -> Running"), \
            "Validator app state changed to 'Running' from 'AboutToBeStarted'"

    def test_device_service_monitor_started_local_support_function(self, remote_conn):
        assert remote_conn.validate_in_logs(
            "[LocalSupportFunction] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "LocalSupportFunction app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[LocalSupportFunction] Starting application ..."), \
            "DSM starting LocalSupportFunction."
        assert remote_conn.validate_in_logs("[LocalSupportFunction] Application started"), \
            "DSM started LocalSupportFunction with a PID."
        assert remote_conn.validate_in_logs(
            "[LocalSupportFunction] Modifying app state from AboutToBeStarted -> Running"), \
            "LocalSupportFunction app state changed to 'Running' from 'AboutToBeStarted'"

    def test_device_service_monitor_started_heartbeat360(self, remote_conn):
        assert remote_conn.validate_in_logs(
            "[Heartbeat360Client] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "Heartbeat360Client app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[Heartbeat360Client] Starting application ..."), \
            "DSM starting Heartbeat360Client."
        assert remote_conn.validate_in_logs("[Heartbeat360Client] Application started"), \
            "DSM started Heartbeat360Client with a PID."
        assert remote_conn.validate_in_logs(
            "[Heartbeat360Client] Modifying app state from AboutToBeStarted -> Running"), \
            "Heartbeat360Client app state changed to 'Running' from 'AboutToBeStarted'"

    def test_device_service_monitor_started_update_handler(self, remote_conn):
        assert remote_conn.validate_in_logs("[UpdateHandler] Modifying app state from NotRunning -> AboutToBeStarted"), \
            "UpdateHandler app state changed to 'AboutToBeStarted' from 'NotRunning'."
        assert remote_conn.validate_in_logs("[UpdateHandler] Starting application ..."), \
            "DSM starting UpdateHandler."
        assert remote_conn.validate_in_logs("[UpdateHandler] Application started"), \
            "DSM started UpdateHandler with a PID."
        assert remote_conn.validate_in_logs("[UpdateHandler] Modifying app state from AboutToBeStarted -> Running"), \
            "UpdateHandler app state changed to 'Running' from 'AboutToBeStarted'"
