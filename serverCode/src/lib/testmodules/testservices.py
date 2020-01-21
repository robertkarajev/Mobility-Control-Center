import sshtunnel as ssh

class SSHTunnel:
    def __init__(self, server_address, server_port, username, password, db_server_address, db_server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.username = username
        self.password = password
        self.db_server_address = db_server_address
        self.db_server_port = db_server_port
        
    def createSSHTunnelForwarder(self):
        self.tunnelForwarder = ssh.SSHTunnelForwarder(ssh_address_or_host = (self.server_address, self.server_port),
                                             ssh_username = self.username,
                                             ssh_password = self.password,
                                             remote_bind_address = (self.db_server_address, self.db_server_port))
        return self.tunnelForwarder

    def startTunnel(self):
        self.tunnelForwarder.start()

    def closeTunnel(self):
        self.tunnelForwarder.stop()