import socket


def get_messages_from_json_metric(metric, prefix=None):
    plugin = metric["plugin"]
    plugin_instance = metric["plugin_instance"]
    host = metric["host"]
    timestamp = metric["time"]

    if plugin_instance:
        plugin = f"{plugin}-{plugin_instance}"

    _type = metric["type"]
    type_instance = metric["type_instance"]
    if type_instance:
        _type = f"{_type}-{type_instance}"

    for name, value in zip(metric["dsnames"], metric["values"]):
        path = f"{host}.{plugin}.{_type}"
        if prefix:
            path = f"{prefix}.{path}"

        if name != "value":
            path = f"{path}.{name}"

        yield f"{path} {value} {timestamp}"


class CarbonClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.sock = socket.create_connection((self.host, self.port), 5)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

    def send(self, message):
        self.sock.sendall(f"{message}\n".encode())
