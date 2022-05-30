from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from todo_list.settings_local import SERVER_VERSION


class AboutView(View):
    def get(self, request):
        context = {
            'server_version': SERVER_VERSION
        }
        return render(
            request,
            'note_api/about.html', context=context
        )


class AboutTemplateView(TemplateView):
    template_name = 'note_api/about.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['server_version'] = SERVER_VERSION

        return contex
