from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from django import template
from django.utils.html import format_html
from django.urls import reverse

if TYPE_CHECKING:
    from django.template.context import RequestContext
    from django.utils.safestring import SafeString

from core.business_logic.services import get_elements_all_by_menu_name

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context: RequestContext, menu_name: str) -> SafeString:
    """
    Custom template tag for drawing a menu.

    Args:
        context (RequestContext): The RequestContext object.
        menu_name (str): The name of the menu.

    Returns:
        SafeString: HTML string representing the menu.
    """

    paths = context['menu_path']
    paths = paths.split('/') if paths else None
    all_elements = get_elements_all_by_menu_name(menu_name=menu_name)

    if not all_elements:
        return format_html(f'The menu "{menu_name}" does not exist.')

    elements_tree = {}

    html_string = '<div class="content__menu">'


    """
    We are converting the data from the request into a dictionary for more
    convenient searching by the parent ID of each element. 
    
    We get a dictionary - 
    {parent_id: {children1_name: children1_pk, children2_name: children2_pk}"
    """
    for element in all_elements:
        parent_pk = element.parent.pk if element.parent else None
        if not elements_tree.get(parent_pk):
            elements_tree[parent_pk] = {element.name: element.pk}
        else:
            elements_tree[parent_pk][element.name] = element.pk


    """
    HTML is generated in case nothing is passed in the query string or
    if the menu name does not match the one in the query string.
    """
    if not paths or paths[0] != menu_name:
        html_string += f'<div class="menu__submenu submenu_{1}">'
        for element_name in elements_tree[None]:
            html_string += (
            f'<a class="menu__element link button" href="{reverse("core:index", kwargs={"menu_path": f"{menu_name}/{element_name}"})}">{element_name}</a>'
        )
        html_string += '</div></div>'
        return format_html(html_string)


    html_generator = GenerateHTML(
        paths=paths,
        elements_tree=elements_tree,
        menu_name=menu_name
    )

    html_generator.generate_html()

    return format_html(html_generator.html_string)


class GenerateHTML:
    def __init__(
            self,
            paths: list[str],
            elements_tree: dict[Optional[str], dict[str, int]],
            menu_name: str
    ) -> None:
        """
        Initializes the GenerateHTML class.

        Args:
            paths (list[str]): List of paths.
            elements_tree (dict[Optional[str], dict[str, int]]): Dictionary 
            representing the elements tree.
            menu_name (str): Name of the menu.
        """
        self._elements_tree = elements_tree
        self._root_element_pk = None
        self._element_url = menu_name + '/'
        self._paths = paths
        self.html_string = ''

    def generate_html(
            self,
            element_index: int = 1,
            url: Optional[str] = None
    ) -> None:
        """
        Generates HTML based on the provided paths and elements tree.

        Args:
            element_index (int, optional): Index of the current element.
            Defaults to 1.
            url (Optional[str], optional): URL of the current element.
            Defaults to None.
        """
        if not url:
            url = self._element_url

        if len(self._paths) > element_index:     
            element = self._paths[element_index]
            if element in self._elements_tree.get(self._root_element_pk, {}):
                self.html_string += f'<div class="menu__submenu">'
                for element_name in self._elements_tree.get(
                    self._root_element_pk,
                    {}
                ):
                    self.html_string += (
                        f'<a class="menu__element link button" href="{reverse("core:index", kwargs={"menu_path": f"{url + element_name}"})}">{element_name}</a>'
                    )
                    if element_name == element:
                        self._root_element_pk = self._elements_tree.get(
                            self._root_element_pk,
                            {}
                        ).get(element)
                        self.generate_html(
                            element_index + 1,
                            url=url + element_name + '/'
                        )
                self.html_string += '</div>'
        else:
            self.html_string += f'<div class="menu__submenu">'
            for element_name in self._elements_tree.get(
                self._root_element_pk,
                {}
            ):
                self.html_string += (
                    f'<a class="menu__element link button" href="{reverse("core:index", kwargs={"menu_path": f"{url + element_name}"})}">{element_name}</a>'
                )
            self.html_string += '</div>'
