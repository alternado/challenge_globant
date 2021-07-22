from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'usuario': False,
        })
        return context


class ListDealView(TemplateView):
    template_name = 'list_deals.html'
    context_object_name = 'deals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'parameter_search': self.request.GET.get('parameter_search', '').strip(),
            'token': self.request.GET.get('token', '')
        })
        return context
