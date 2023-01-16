from django.urls import path

from med_catalog.views import (get_refbook_versions,
                               get_version_elements, check_version_elements)


urlpatterns = [
    path('', get_refbook_versions, name='refbooks'),
    path('<int:id>/elements/', get_version_elements, name='get_elements'),
    path(
        '<int:id>/check_element/',
        check_version_elements,
        name='check_element'
    )
]
