from django.urls import path

from core.presentation.views import index_controller


app_name = 'core'

urlpatterns = [
    path('<path:menu_path>/', index_controller, name='index'),
    path('', index_controller, name='index')
]
