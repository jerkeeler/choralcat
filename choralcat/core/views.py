import logging

from django.views.generic import CreateView, UpdateView

logger = logging.getLogger(__name__)


class UserCreateView(CreateView):
    def form_valid(self, form):
        logger.info(f"{form.instance.__class__.__name__} {form.instance} created by {self.request.user}")
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    def form_valid(self, form):
        logger.info(f"{form.instance.__class__.__name__} {form.instance} updated by {self.request.user}")
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
