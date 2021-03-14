import json

from django.core.exceptions import (
    ValidationError,
    PermissionDenied,
)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import MetricConfig
from .utils import (
    get_messages_from_json_metric,
    CarbonClient,
)


@csrf_exempt
@require_POST
def proxy(request):
    token = request.headers.get("X-Proxy-Token")
    try:
        config = MetricConfig.objects.get(token=token)
    except (MetricConfig.DoesNotExist, ValidationError):
        raise PermissionDenied

    payload = request.body.decode()
    metrics = json.loads(payload)

    with CarbonClient(config.carbon_host, config.carbon_port) as client:
        for metric in metrics:
            for message in get_messages_from_json_metric(metric, config.prefix):
                client.send(message)

    return HttpResponse("OK")
