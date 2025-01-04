# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# from rest_framework.response import Response
# from rest_framework import permissions
# from rest_framework.views import APIView
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.utils.decorators import method_decorator

# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class GetCSRFToken(APIView):
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, format=None):
#         return Response({ 'success': 'CSRF cookie set' })


def login_view(request):
    if not request.COOKIES.get('mort_session', False):
        res = request.session.create()
    form = LoginForm(request.POST or None)

    msg = None
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})