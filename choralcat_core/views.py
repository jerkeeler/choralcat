from django.views.generic import CreateView, UpdateView


class UserCreateView(CreateView):
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
