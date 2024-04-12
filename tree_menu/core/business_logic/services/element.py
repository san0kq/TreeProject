from core.models import Element


def get_elements_all_by_menu_name(menu_name: str) -> list[Element]:
    """
    Retrieves all elements associated with a given menu name.

    Args:
        menu_name (str): The name of the menu to retrieve elements from.

    Returns:
        list[Element]: A list of Element objects associated with the
        specified menu name.
    """
    all_elements = list(
        Element.objects.filter(menu__name=menu_name)
        .select_related('menu', 'parent')
    )
    return all_elements
