from django.views.generic.base import TemplateView


class CallBackView(TemplateView):
    template_name = "artd_shopify/callback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context