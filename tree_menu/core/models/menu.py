from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Element(models.Model):
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
