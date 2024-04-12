from django import template
from django.utils.html import format_html
from django.urls import reverse

from core.models import Menu, Element

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name: str):
    paths = context['menu_path']
    paths = paths.split('/') if paths else None
    all_elements = list(Element.objects.filter(menu__name='Menu1').select_related('menu'))
    elements_tree = {}
    root_element_pk = None
    element_url = menu_name + '/'
    html_string = ''

    for element in all_elements:
        parent_pk = element.parent.pk if element.parent else None
        if not elements_tree.get(parent_pk):
            elements_tree[parent_pk] = {element.name: element.pk}
        else:
            elements_tree[parent_pk][element.name] = element.pk
    if not paths or paths[0] != menu_name:
        for element_name in elements_tree[None]:
            html_string += f'<a href="{reverse("core:index", kwargs={"menu_path": f"{menu_name}/{element_name}"})}">{element_name}</a>'
        return format_html(html_string)

    for path in paths[1::]:
        if path in elements_tree.get(root_element_pk, {}):
            for element_name in elements_tree.get(root_element_pk, {}):
                html_string += f'<a href="{reverse("core:index", kwargs={"menu_path": f"{element_url + element_name}"})}">{element_name}</a>'
            element_url += path + '/'
            root_element_pk = elements_tree.get(root_element_pk, {}).get(path)
        else:
            break
    print(elements_tree)
    if len(paths) > 1:
        for element_name in elements_tree.get(root_element_pk, {}):
            html_string += f'<a href="{reverse("core:index", kwargs={"menu_path": f"{element_url + element_name}"})}">{element_name}</a>'

    return format_html(html_string)
