from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class PushView(TemplateView):
    template_name = 'push/web.html'
