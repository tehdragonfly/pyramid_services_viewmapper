pyramid_services_viewmapper
===========================

An extension for the Pyramid web framework.

`pyramid_services_viewmapper` provides a [view mapper](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#using-a-view-mapper)
for use in conjunction with [pyramid_services](https://github.com/mmerickel/pyramid_services).
It extends the functionality of `pyramid_services` to provide *dependency
injection*: you can add custom arguments to your view functions, and
the view mapper will automatically populate those arguments with matching
services.

Setup
-----

Register the view mapper in your `Configurator`:

    from pyramid_services_viewmapper import ServiceViewMapper
    config.set_view_mapper(ServiceViewMapper)

Usage
-----

Services registered by interface alone are injected by a simple type
annotation. For example this...

    @view_config(route_name="home", renderer="json")
    def home(request, login_svc: ILoginService):
        token = login_svc.create_token_for_login(name)
        return {"access_token": token}

...is equivalent to this:

    @view_config(route_name="home", renderer="json")
    def home(request):
        login_svc = request.find_service(ILoginService)
        token = login_svc.create_token_for_login(name)
        return {"access_token": token}

Services registered by name can be injected using a `ServiceInjector` object.
For example this...

    from pyramid_services_viewmapper import ServiceInjector as S

    @view_config(route_name="users", renderer="json")
    def users(request, db: S(name="db")):
        users = db.query(User)
        return {"users": users}

...is equivalent to this:

    @view_config(route_name="users", renderer="json")
    def users(request):
        db = request.find_service(name="db")
        users = db.query(User)
        return {"users": users}

The `ServiceInjector` class can be used as a shortcut for this:

    from pyramid_services_viewmapper import ServiceInjector as S

    @view_config(route_name="users", renderer="json")
    def users(request, db: S):
        users = db.query(User)
        return {"users": users}
