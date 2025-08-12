from django.conf import settings


def get_drf_spectacular_view_decorator(endpoint_group):
    """
    Get drf spectacular view decorator.
    """

    def activate_drf_spectacular_view_decorator(view):
        """
        If DEBUG=True, select view decorator for specified view.
        """
        if not settings.SHOULD_SHOW_DOCS:
            return view

        from apps.api.v1.api_docs.view_decorators import VIEW_DECORATORS

        view_name = view.view_class.__name__ if view.__class__.__name__ == "function" else view.__name__
        return VIEW_DECORATORS[endpoint_group][view_name](view)

    return activate_drf_spectacular_view_decorator
