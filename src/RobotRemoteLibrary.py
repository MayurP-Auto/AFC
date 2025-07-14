import paramiko
import threading
import time


class RobotRemoteLibrary:
    """
    A dedicated library for Robot Framework to manage remote SSH connections and logs.
    This version includes enhanced debugging and pre-checks.
    """

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.hostname = None
        self.username = None
        self.password = None
        self.log_buffer = []
        self._log_stream_thread = None
        self._stop_streaming = threading.Event()

    def open_connection(self, host, user, password):
        self.hostname = host
        self.username = user
        self.password = password

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        print(f"Connecting to {self.hostname}...")
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password, timeout=20)
        print("Connected")

    def close_connection(self):
        if self._log_stream_thread and self._log_stream_thread.is_alive():
            self._stop_streaming.set()
            self._log_stream_thread.join(timeout=5)
            print("Log streaming thread stopped.")

        if self.client:
            self.client.close()
            print("Connection closed.")

    def check_remote_file_exists(self, file_path):
        """Checks if a file exists and is accessible on the remote host."""
        print(f"[DEBUG] Checking for file: {file_path}")
        command = f'ls "{file_path}"'
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code == 0:
            print(f"[DEBUG] File '{file_path}' found.")
            return True
        else:
            error_message = stderr.read().decode().strip()
            print(f"[DEBUG] File check failed. Exit code: {exit_code}, Error: {error_message}")
            return False

    def get_latest_service_start_line(self, log_path, log_name, marker):
        command = f'grep -n "{marker}" "{log_path}/{log_name}" | tail -1 | cut -d":" -f1'
        stdin, stdout, stderr = self.client.exec_command(command)
        line_number = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error:
            print(f"Error while searching for startup line: {error}")

        if line_number.isdigit():
            print(f"Latest startup line number: {line_number}")
            return int(line_number)
        else:
            print(f"Startup marker '{marker}' not found.")
            return None

    def _stream_logs(self, command):
        """
        Private method to handle log streaming with a more robust implementation.
        """
        lines_read = 0
        try:
            stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
            print(f"[STREAM DEBUG] Executed command: {command}")
            print("[STREAM DEBUG] Log streaming thread started. Waiting for lines...")

            for line in iter(stdout.readline, ""):
                if self._stop_streaming.is_set():
                    break

                if line:
                    lines_read += 1
                    line_clean = line.strip()
                    print(f"[STREAM DEBUG] Read line: {line_clean}")
                    self.log_buffer.append(line_clean)

            if stderr.channel.recv_stderr_ready():
                err_output = stderr.read().decode().strip()
                if err_output:
                    print(f"[STREAM DEBUG] Stderr output from command: {err_output}")

        except Exception as e:
            print(f"[STREAM DEBUG] An exception occurred in the log streaming thread: {e}")
        finally:
            print(f"[STREAM DEBUG] Thread exiting. Total lines read: {lines_read}. Buffer size: {len(self.log_buffer)}")

    def start_log_stream_from_latest_restart(self, log_path, log_name, marker):
        if not self.check_remote_file_exists(f"{log_path}/{log_name}"):
            raise RuntimeError(f"Log file not found or not accessible at {log_path}/{log_name}")

        line_number = self.get_latest_service_start_line(log_path, log_name, marker)

        # DIAGNOSTIC STEP: Removing 'stdbuf -oL' to check if it's the cause of the crash.
        if line_number is None:
            print("Service start marker not found. Tailing from the end of the log.")
            command = f'tail -n 0 -f "{log_path}/{log_name}"'
        else:
            print(f"Starting log stream from line {line_number}")
            command = f'tail -n +{line_number} -f "{log_path}/{log_name}"'

        print(f"[DEBUG] Preparing to execute remote command for streaming: {command}")

        self._stop_streaming.clear()
        self._log_stream_thread = threading.Thread(
            target=self._stream_logs,
            args=(command,),
            daemon=True
        )
        self._log_stream_thread.start()
        print("Log streaming thread initiated.")

        time.sleep(1)
        if not self._log_stream_thread.is_alive():
            raise RuntimeError(
                "Log streaming thread failed to start or died immediately. The remote command may be invalid (e.g., 'stdbuf' not found) or file permissions may be incorrect.")

    def validate_in_logs(self, text_to_find):
        for line in reversed(self.log_buffer):
            if text_to_find in line:
                return True
        return False

    def get_log_buffer_for_debug(self):
        """Returns the current log buffer as a printable string for debugging."""
        if not self.log_buffer:
            return "--- Log buffer is empty ---"
        return " ||| ".join(line.strip() for line in self.log_buffer)

    def is_service_crashing(self, log_path, log_name, marker, min_wait=2, max_wait=20):
        initial_count = self.count_marker_occurrences(log_path, log_name, marker)

        wait_duration = max_wait - min_wait
        if wait_duration <= 0:
            wait_duration = 2

        print(f"Checking for crashes for {wait_duration} seconds...")
        time.sleep(wait_duration)

        current_count = self.count_marker_occurrences(log_path, log_name, marker)
        if current_count - initial_count > 1:
            return True
        return False

    def count_marker_occurrences(self, log_path, log_name, marker):
        command = f'grep -c "{marker}" "{log_path}/{log_name}"'
        stdin, stdout, stderr = self.client.exec_command(command)
        count = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if error and "No such file" not in error:
            print(f"Error counting marker: {error}")
        return int(count) if count.isdigit() else 0
