# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def data_table(request: WSGIRequest) -> HttpResponse:
    context = {
        "content": request.path,
    }
    return render(request, "menu.html", context=context)
