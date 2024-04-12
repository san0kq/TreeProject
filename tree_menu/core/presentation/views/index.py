from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def index_controller(
        request: HttpRequest,
        menu_path: str = None
    ) -> HttpResponse:
    """
    Controller function for rendering the index page.

    Args:
        request (HttpRequest): The HTTP request object.
        menu_path (str, optional): The path to the menu. Defaults to None.

    Returns:
        HttpResponse: The HTTP response object.
    """
    context = {'menu_path': menu_path}
    return render(request, 'index.html', context=context)
