# gwh ![badge](https://github.com/kviktor/gwh/actions/workflows/django.yml/badge.svg)

colltectd -> carbon write_http proxy. This way you can have a protected carbon endpoint if you can't whitelist your IP.

(nam based on **g**raphite **w**rite **h**ttp, which doesn't make much sense but it's short)

# setup

First create a superuser (`./manage.py createsuperuser`) then in the admin create a new MetricConfig.

On your machine edit your collectd config and set something like this, change the uuid to the one from your own MetricConfig

```
<Plugin write_http>
	<Node "example">
		URL "https://your.domain/api/proxy/"
		Header "X-Proxy-Token: 2485feb3-9020-488e-a133-aae32d0ea80d"
		Format "JSON"
		Metrics true
		Notifications false
		StoreRates false
		BufferSize 4096
		LowSpeedLimit 0
		Timeout 0
	</Node>
</Plugin>
```

For more info visit: https://collectd.org/wiki/index.php/Plugin:Write_HTTP
