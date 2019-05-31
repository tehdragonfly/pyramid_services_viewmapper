from __future__ import annotations

from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from zope.interface import Interface, implementer

from pyramid_services_viewmapper import ServiceViewMapper


class IExampleService(Interface):
    def example(self):
        pass


@implementer(IExampleService)
class ExampleService:
    def example(self):
        return "example"


def function_view(request, example_service: IExampleService):
    return {"function": example_service.example()}


class ClassView:
    def __init__(self, request, example_service: IExampleService):
        self.request = request
        self.example_service = example_service

    def __call__(self):
        return {"class": self.example_service.example()}


if __name__ == '__main__':
    config = Configurator()

    config.include("pyramid_services")
    config.register_service(ExampleService(), IExampleService)

    config.set_view_mapper(ServiceViewMapper)

    config.add_route("function", "/function")
    config.add_view(function_view, route_name="function", renderer="json")

    config.add_route("class", "/class")
    config.add_view(ClassView, route_name="class", renderer="json")

    server = make_server('0.0.0.0', 8080, config.make_wsgi_app())
    server.serve_forever()