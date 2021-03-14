from unittest import mock
import json

from django.test import (
    Client,
    TestCase,
)

from gwh import models


class ProxyTest(TestCase):
    def setUp(self):
        self.conf = models.MetricConfig(
            name="test",
            carbon_host="host",
            carbon_port=12345,
            prefix="pre",
        )
        self.conf.save()

    def test_invalid_token(self):
        resp = Client().post("/api/proxy/", {}, HTTP_X_PROXY_TOKEN="not uuid")
        self.assertEqual(resp.status_code, 403)

    def test_no_token(self):
        resp = Client().post("/api/proxy/")
        self.assertEqual(resp.status_code, 403)

    def test_non_existent_token(self):
        resp = Client().post(
            "/api/proxy/",
            {},
            HTTP_X_PROXY_TOKEN="0169306c-cef4-4bf1-aef0-9bfe20959f0c",
        )
        self.assertEqual(resp.status_code, 403)

    @mock.patch("gwh.views.CarbonClient")
    @mock.patch("gwh.views.get_messages_from_json_metric")
    def test_valid_token(self, p_get, p_client):
        p_get.return_value = ["mocked"]

        resp = Client().generic(
            "POST",
            "/api/proxy/",
            json.dumps(
                [
                    {
                        "test": True,
                    },
                ]
            ),
            HTTP_X_PROXY_TOKEN=self.conf.token,
        )

        p_get.assert_called_once_with({"test": True}, "pre")
        p_client().__enter__().send.assert_called_once_with("mocked")
        self.assertEqual(resp.status_code, 200)
