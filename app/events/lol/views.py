from django.views.generic import TemplateView

from events.lol.models import Player


class IndexView(TemplateView):
    template_name = 'events/lol/index.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.all()
        return context
