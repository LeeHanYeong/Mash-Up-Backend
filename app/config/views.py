from django.views.generic import TemplateView

__all__ = (
    "IndexView",
    "PushView",
)


class IndexView(TemplateView):
    template_name = "index.jinja2"


class PushView(TemplateView):
    template_name = "push/web.html"
