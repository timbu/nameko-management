import json
import os
import socket
from datetime import datetime
from logging import getLogger

from nameko.extensions import DependencyProvider


log = getLogger(__file__)


class RuntimeStats(DependencyProvider):
    """
    Tracks basic runtime worker stats.
    Could easily be made to track current error/success rates etc.
    """

    def __init__(self):
        self.running_workers = {}

    def worker_setup(self, worker_ctx):
        try:
            self.running_workers[worker_ctx.call_id] = (
                worker_ctx.entrypoint.method_name,
                datetime.utcnow(),
            )
        except Exception as exc:
            log.error(exc)

    def worker_result(self, worker_ctx, result=None, exc_info=None):
        try:
            self.running_workers.pop(worker_ctx.call_id)
        except Exception as exc:
            log.error(exc)

    def management_stats(self):
        now = datetime.utcnow()
        running_stats = [
            {
                'entrypoint': entrypoint,
                'call_id': call_id,
                'start': start.isoformat(),
                'time': (now - start).total_seconds()
            }
            for call_id, (entrypoint, start) in self.running_workers.items()
        ]
        return {
            'running_workers': sorted(running_stats, key=lambda x: x['time']),
        }


class ServerInfo(DependencyProvider):

    @property
    def version_file(self):
        config = self.container.config.copy()
        return config.get('VERSION_FILE')

    def get_version_info(self):
        version_info = None
        version_file = self.version_file
        if version_file and os.path.isfile(version_file):
            with open(version_file, 'r') as data_file:
                version_info = json.load(data_file)
        return version_info

    def setup(self):
        self.hostname = socket.gethostname()
        self.starttime = datetime.utcnow()
        self.version_info = self.get_version_info()
        self.service_name = self.container.service_name

    def get_dependency(self, worker_ctx):
        return self

    def get_server_info(self):
        return {
            'hostname': self.hostname,
            'uptime': (datetime.utcnow() - self.starttime).total_seconds(),
            'version_info': self.version_info,
            'service_name': self.service_name,
        }

    def management_stats(self):
        return self.get_server_info()

    def management_healthcheck(self):
        return self.get_server_info()
