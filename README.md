pyramid_services_viewmapper
===========================

An extension for the Pyramid web framework.

`pyramid_services_viewmapper` provides a [view mapper](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#using-a-view-mapper)
for use in conjunction with [pyramid_services](https://github.com/mmerickel/pyramid_services).
It extends the functionality of pyramid_services to provide *dependency
injection*: you can add custom arguments to your view functions, and
`pyramid_services_viewmapper` will automatically populate those arguments with
matching services.

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
