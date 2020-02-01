from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from afol_toolbox_app.view.base_view import get_base_context


def view(request: WSGIRequest) -> HttpResponse:
    return render(request, "index.html", get_base_context(request))
