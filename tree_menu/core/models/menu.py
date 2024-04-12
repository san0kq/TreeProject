from django.db import models


class Menu(models.Model):
    """
    Represents a menu in the application.

    Attributes:
    - name (CharField): The name of the menu. Limited to a maximum length of
      16 characters.

    Methods:
    - __str__(): Returns the name of the menu as a string.
    """
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Element(models.Model):
    """
    Represents an element in the application, which can be associated with
    a menu.

    Attributes:
    - name (CharField): The name of the element. Limited to a maximum length
      of 32 characters.
    - parent (ForeignKey): Represents the parent element of the current
      element. It allows elements to have hierarchical relationships.
      Can be null.
    - menu (ForeignKey): Represents the menu to which the element belongs.

    Methods:
    - __str__(): Returns the name of the element as a string.
    """
    name = models.CharField(max_length=32)
    parent = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.SET_NULL
    )
    menu = models.ForeignKey(
        to=Menu,
        related_name='element',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
