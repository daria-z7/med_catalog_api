from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from ..models import Refbook, Version, Element


class RefbookViewTest(APITestCase, URLPatternsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.refbook = Refbook.objects.create(
            code='Тестовый код',
            name='Тестовое имя',
            description='Тестовое описание',
        )
        cls.version = Version.objects.create(
            refbook_id=cls.refbook,
            version='Тестовая группа',
            date_start='2023-01-13'
        )
        cls.element = Element.objects.create(
            version_id=cls.version,
            code='Тестовый код элемента',
            value='Тестовое значение'
        )
    urlpatterns = [
        path('refbooks/', include('med_catalog.urls')),
    ]

    def test_get_refbook(self):
        """Проверяет код ответа и кол-во полученных справочников.
        """
        url = reverse('refbooks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_elements_200(self):
        """Проверяет код ответа и кол-во полученных элементов.
        """
        response = self.client.get(
            reverse('get_elements', kwargs={'id': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_elements_404(self):
        """Проверяет, что вернется 404, при указании несуществующего
        id справочника.
        """
        response = self.client.get(
            reverse('get_elements', kwargs={'id': 2}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_elements_obligatory_params(self):
        """Проверяет, что вернется 400, если не указать код и значение
        элемента в запросе.
        """
        response = self.client.get(
            reverse('check_element', kwargs={'id': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
