from unittest import mock

from django.test import TestCase

from gwh import utils


class GetMessagesFromJsonMetricTest(TestCase):
    def test_plugin_instance(self):
        metric = {
            "values": [10],
            "dstypes": ["counter"],
            "dsnames": ["value"],
            "time": 12345,
            "interval": 10,
            "host": "hostname",
            "plugin": "disk",
            "plugin_instance": "sda",
            "type": "disk_octets",
            "type_instance": ""
        }

        self.assertEqual(
            ["hostname.disk-sda.disk_octets 10 12345"],
            list(utils.get_messages_from_json_metric(metric))
        )

    def test_no_plugin_instance(self):
        metric = {
            "values": [10],
            "dstypes": ["counter"],
            "dsnames": ["value"],
            "time": 12345,
            "interval": 10,
            "host": "hostname",
            "plugin": "disk",
            "plugin_instance": "",
            "type": "disk_octets",
            "type_instance": ""
        }

        self.assertEqual(
            ["hostname.disk.disk_octets 10 12345"],
            list(utils.get_messages_from_json_metric(metric))
        )

    def test_type_instance(self):
        metric = {
            "values": [10],
            "dstypes": ["counter"],
            "dsnames": ["value"],
            "time": 12345,
            "interval": 10,
            "host": "hostname",
            "plugin": "disk",
            "plugin_instance": "",
            "type": "disk_octets",
            "type_instance": "ti"
        }

        self.assertEqual(
            ["hostname.disk.disk_octets-ti 10 12345"],
            list(utils.get_messages_from_json_metric(metric))
        )

    def test_with_prefix(self):
        metric = {
            "values": [10],
            "dstypes": ["counter"],
            "dsnames": ["value"],
            "time": 12345,
            "interval": 10,
            "host": "hostname",
            "plugin": "disk",
            "plugin_instance": "sda",
            "type": "disk_octets",
            "type_instance": ""
        }

        self.assertEqual(
            ["testing.hostname.disk-sda.disk_octets 10 12345"],
            list(utils.get_messages_from_json_metric(metric, prefix="testing"))
        )

    def test_custom_value(self):
        metric = {
            "values": [10],
            "dstypes": ["counter"],
            "dsnames": ["rx"],
            "time": 12345,
            "interval": 10,
            "host": "hostname",
            "plugin": "disk",
            "plugin_instance": "sda",
            "type": "disk_octets",
            "type_instance": ""
        }

        self.assertEqual(
            ["hostname.disk-sda.disk_octets.rx 10 12345"],
            list(utils.get_messages_from_json_metric(metric))
        )


class CarbonClientTest(TestCase):

    @mock.patch("gwh.utils.socket")
    def test_client(self, p_socket):
        p_sock = mock.Mock()
        p_socket.create_connection.return_value = p_sock

        with utils.CarbonClient("host", 12345) as client:
            p_socket.create_connection.assert_called_once_with(("host", 12345), mock.ANY)
            client.send("message")
            p_sock.sendall.assert_called_once_with(b"message\n")

            p_sock.close.assert_not_called()

        p_sock.close.assert_called_once_with()
