"""afol_toolbox_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from afol_toolbox_app.model.menu import menu_items
from afol_toolbox_app.view import menu


def get_urls_for_item(item: menu_items.MenuItem) -> list:
    if isinstance(item, menu_items.Folder):
        result = []
        for it in item.children:
            result.extend(get_urls_for_item(it))
        return result
    elif isinstance(item, menu_items.Tool):
        return [path(item.absolute_url[1:], item.view_func)]


def get_urls_from_menu() -> list:
    result = []
    for it in menu_items.get_menu():
        result.extend(get_urls_for_item(it))
    return result


urlpatterns = [
    path("", menu.view),
    *get_urls_from_menu(),
]
