import paramiko


class RemoteConnection:
    def __init__(self, host, user, password):
        self.client = paramiko.SSHClient()
        self.hostname = host
        self.username = user
        self.password = password
        # self.log_path = log_path
        # self.log_name = log_name
        self.log_buffer = []

    def open_connection(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        print("Connecting ... ")
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print("Connected")

    def stream_logs(self, log_path, log_name):
        # self.open_connection()
        stdin, stdout, stderr = self.client.exec_command(f'tail -n100 {log_path}/{log_name}')
        output_list = stdout.read().decode()
        # print(output_list)
        return self.log_buffer.append(output_list)

    def parse_logs(self):
        for raw_line in self.log_buffer:
            print(raw_line)
