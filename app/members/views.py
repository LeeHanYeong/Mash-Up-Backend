from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import LoginForm, PasswordSetForm


class LoginView(FormView):
    template_name = "members/login.jinja2"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        data = {k: v for k, v in form.cleaned_data.items() if bool(v)}
        user = authenticate(**data)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error("name", "해당하는 사용자 정보가 없습니다")
            return super().form_invalid(form)


class PasswordSetView(FormView):
    template_name = "members/password-set.jinja2"
    form_class = PasswordSetForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        password = form.cleaned_data["password2"]
        user = self.request.user
        user.set_password(password)
        user.save()
        login(self.request, user, backend="members.backends.NameBackend")
        return super().form_valid(form)
