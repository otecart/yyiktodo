from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View


class RegisterView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy("index")
    template_name = "yyik_auth/register.html"

    def form_valid(self, form: UserCreationForm):
        user = form.save()
        login(self.request, user)
        next = self.request.GET.get("next")
        next = next or self.success_url
        return redirect(next)  # type: ignore


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("index")
    template_name = "yyik_auth/login.html"

    def form_valid(self, form: AuthenticationForm):
        user = form.get_user()
        login(self.request, user)
        next = self.request.GET.get("next")
        next = next or self.success_url
        return redirect(next)  # type: ignore


class LogoutView(View):
    def get(self, request):
        logout(request)
        next = self.request.GET.get("next")
        next = next or "index"
        return redirect(next)  # type: ignore
