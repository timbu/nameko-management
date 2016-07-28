import inspect

from nameko.messaging import Consumer
from nameko.rpc import Rpc
from nameko.web.handlers import HttpRequestHandler

from . import ManagementPlugin, register_plugin

handler_registry = {}


def register_entrypoint_handler(entrypoint_cls):
    def decorator(handler_cls):
        handler_registry[entrypoint_cls] = handler_cls
        return handler_cls
    return decorator


class EntrypointHandler(object):

    def __init__(self, service_cls, entrypoint):
        self.entrypoint = entrypoint
        self.service_cls = service_cls

    def get_result(self):
        ep = self.entrypoint
        method = getattr(self.service_cls, ep.method_name)
        expected_excs = getattr(ep, 'expected_exceptions', tuple()) or tuple()
        expected_excs = (
            expected_excs
            if isinstance(expected_excs, tuple) else [expected_excs]
        )

        return {
            'type': type(ep).__name__,
            'name': ep.method_name,
            # TODO - make signature more readable
            'signature': inspect.getfullargspec(method),
            'doc': inspect.getdoc(method),
            'expected_exceptions': [exc.__name__ for exc in expected_excs]
        }


@register_entrypoint_handler(Rpc)
class RpcHandler(EntrypointHandler):
    def get_result(self):
        result = super(RpcHandler, self).get_result()
        result['sensitive_variables'] = self.entrypoint.sensitive_variables
        return result


@register_entrypoint_handler(HttpRequestHandler)
class HttpHandler(EntrypointHandler):
    def get_result(self):
        result = super(HttpHandler, self).get_result()
        result['http_method'] = self.entrypoint.method
        result['url'] = self.entrypoint.url
        return result


@register_entrypoint_handler(Consumer)
class ConsumerHandler(EntrypointHandler):
    def get_result(self):
        result = super(ConsumerHandler, self).get_result()
        # TODO - confirm requirements
        result['queue_name'] = self.entrypoint.queue.name
        result['exchange_name'] = self.entrypoint.queue.exchange.name
        result['requeue_on_error'] = self.entrypoint.requeue_on_error
        return result


# TODO - eventHandler


@register_plugin
class ListEntrypoints(ManagementPlugin):
    name = 'entrypoints'

    def get_result(self, request):
        results = []
        service_cls = self.container.service_cls
        for ep in self.container.entrypoints:
            for type_ in ep.__class__.mro():
                handler_cls = handler_registry.get(type_)
                if handler_cls:
                    break
            else:
                handler_cls = EntrypointHandler

            handler = handler_cls(service_cls, ep)
            results.append(handler.get_result())

        return results
