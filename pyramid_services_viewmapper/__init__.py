from inspect import isclass, signature
from typing import get_type_hints


class ServiceViewMapper:
    """
    View mapper for use with pyramid_services.

    This uses the annotations on a given view to inject services. For example:

        @view_config(route_name="home", renderer="json")
        def home(request, login_svc: ILoginService):
            token = login_svc.create_token_for_login(name)
            return {"access_token": token}

    Currently it can only find services by interface, not by name.
    """

    def __init__(self, **kw):
        pass

    def __call__(self, view):
        parameters = signature(view).parameters

        annotations = get_type_hints(view.__init__ if isclass(view) else view)
        # TODO named services
        services = [
            (name, interface) for (name, interface) in annotations.items()
            if name not in ("request", "context", "return")
        ]

        def wrapped_view(context, request):
            kwargs = {
                name: request.find_service(interface)
                for name, interface in services
            }
            if "context" in parameters:
                kwargs["context"] = context
            if "request" in parameters:
                kwargs["request"] = request
            if isclass(view):
                return view(**kwargs)()
            return view(**kwargs)

        return wrapped_view
