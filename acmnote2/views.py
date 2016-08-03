from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User


def index_page(request):
    if not request.user.is_authenticated():
        return render(request, "index.html")

    if request.META.get('HTTP_REFERER') or request.GET.get("index"):
        return render(request, "index.html")
    else:
        return render(request, "index.html")
