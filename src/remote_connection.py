import paramiko
import threading
import time


class RemoteConnection:
    def __init__(self, host, user, password):
        self.client = paramiko.SSHClient()
        self.hostname = host
        self.username = user
        self.password = password
        self.log_buffer = []

    def open_connection(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        print("Connecting ... ")
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print("Connected")

    def close_connection(self):
        self.client.close()

    def get_latest_service_start_line(self, log_path, log_name, marker):
        # Find the last line number that contains the marker
        command = (
            f'grep -n "{marker}" {log_path}/{log_name} | tail -1 | cut -d":" -f1'
        )
        stdin, stdout, stderr = self.client.exec_command(command)
        line_number = stdout.read().decode().strip()
        error = stderr.read().decode()
        if error:
            print("Error while searching for startup line:", error)
        print(f"Latest startup line number: {line_number}")
        if line_number.isdigit():
            return int(line_number)
        else:
            return None

    def stream_logs_from_latest_start(self, log_path, log_name, marker):
        line_number = self.get_latest_service_start_line(log_path, log_name, marker)
        if line_number is None:
            print("Service start marker not found. Starting from end of log.")
            command = f'tail -f {log_path}/{log_name}'
        else:
            print(f"Starting log stream from line {line_number}")
            command = f'tail -n +{line_number} -f {log_path}/{log_name}'

        stdin, stdout, stderr = self.client.exec_command(command)
        print("Started streaming logs...")
        for line in iter(stdout.readline, ""):
            if line:
                # print(line.strip())  # Optional: print logs live
                self.log_buffer.append(line)

    def start_log_stream_from_latest_restart(self, log_path, log_name, marker):
        thread = threading.Thread(
            target=self.stream_logs_from_latest_start,
            args=(log_path, log_name, marker),
            daemon=True
        )
        thread.start()

    def validate_in_logs(self, log):
        for line in reversed(self.log_buffer):
            if log in line:
                print("Case Passed")
                print(line)
                return True
        print("Case Failed")
        return False

    def is_service_crashing(self, log_path, log_name, marker, min_wait=2, max_wait=20):
        """
        Heuristically detects service crash/restarts by checking for multiple marker entries
        in a short time window.
        """
        initial_count = self.count_marker_occurrences(log_path, log_name, marker)

        for second in range(min_wait, max_wait + 1):
            time.sleep(1)
            current_count = self.count_marker_occurrences(log_path, log_name, marker)
            if current_count - initial_count > 1:
                return True
        return False

    def count_marker_occurrences(self, log_path, log_name, marker):
        command = f'grep "{marker}" {log_path}/{log_name} | wc -l'
        stdin, stdout, stderr = self.client.exec_command(command)
        count = stdout.read().decode().strip()
        return int(count) if count.isdigit() else 0
