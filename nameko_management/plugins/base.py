import json
from logging import getLogger

from nameko.exceptions import serialize
from werkzeug.routing import Rule
from werkzeug.wrappers import Response

log = getLogger(__file__)


plugin_registry = {}


def register_plugin(cls):
    plugin_registry[cls.name] = cls
    return cls


class ManagementPlugin:
    name = None

    def __init__(self, container):
        self.container = container

    @property
    def url_root(self):
        return '/management/'

    @property
    def url(self):
        return '{}{}'.format(self.url_root, self.name)

    @property
    def method(self):
        return 'GET'

    def get_url_rule(self):
        return Rule(self.url, methods=[self.method])

    def handle_request(self, request):
        try:
            result = self.get_result(request)
            return Response(
                json.dumps(result),
                status=200,
                headers=None,
            )
        except Exception as exc:
            log.error(exc)
            error_dict = serialize(exc)
            payload = u'Error: {exc_type}: {value}\n'.format(**error_dict)
            return Response(
                payload,
                status=500,
            )

    def get_result(self, request):
        raise NotImplementedError()


@register_plugin
class StatsPlugin(ManagementPlugin):
    name = 'stats'

    def get_result(self, request):
        return self.gather_stats()

    def gather_stats(self):
        stats = {}
        for dep in self.container.dependencies:
            try:
                stats[dep.attr_name] = dep.management_stats()
            except AttributeError:
                pass
        return stats


@register_plugin
class HealthcheckPlugin(ManagementPlugin):
    name = 'healthcheck'

    def get_result(self, request):
        result = {}
        for dep in self.container.dependencies:
            try:
                result[dep.attr_name] = dep.management_healthcheck()
            except AttributeError:
                pass
        return result
