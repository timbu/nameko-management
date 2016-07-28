import inspect

from . import ManagementPlugin, register_plugin


@register_plugin
class ListEntrypoints(ManagementPlugin):
    name = 'entrypoints'

    def get_result(self, request):
        results = []
        service_cls = self.container.service_cls
        for ep in self.container.entrypoints:
            method = getattr(service_cls, ep.method_name)
            # TODO - customise info for each entrypoint type
            # URL rules for http, sensitive vars for rpc, queue names for
            # consumers etc?
            results.append({
                'type': type(ep).__name__,
                'name': ep.method_name,
                # TODO - make signature more readable
                'signature': inspect.getfullargspec(method),
                'doc': inspect.getdoc(method),
                # TODO 'expected_exceptions'?
            })
        return results
