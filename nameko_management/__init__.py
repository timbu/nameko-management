from logging import getLogger

from nameko.extensions import DependencyProvider
from nameko.web.server import WebServer, parse_address

from .dependencies import RuntimeStats, ServerInfo
from .plugins import plugin_registry

log = getLogger('nameko-management')


class ManagementWebServer(WebServer):

    def start(self):
        super(ManagementWebServer, self).start()
        log.info("listening at: %s", self.bind_addr)

    @property
    def bind_addr(self):
        address_str = self.container.config.get(
            "MANAGEMENT_WEB_SERVER_CONFIG", '0.0.0.0:8980')
        return parse_address(address_str)


class Management(DependencyProvider):
    """
    "management" dependency that does not use the worker pool.
    So we can perform management actions even when we are at max workers.
    """
    server = ManagementWebServer()

    def get_dependency(self, worker_ctx):
        return self

    def setup(self):
        plugin_instances = [
            cls(self.container) for cls in plugin_registry.values()
        ]
        self.plugin_map = {
            plugin.name: plugin for plugin in plugin_instances
        }
        for plugin in plugin_instances:
            self.server.register_provider(plugin)
            log.info(
                'registered plugin: %s at %s',
                plugin.name,
                plugin.get_url_rule()
            )

    def stop(self):
        for plugin in self.plugin_map.values():
            self.server.unregister_provider(plugin)
        super(Management, self).stop()


class ManagementServiceMixin(object):
    managment = Management()
    server_info = ServerInfo()
    runtime_stats = RuntimeStats()
