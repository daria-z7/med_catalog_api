from django.test import TestCase
from sqlite3 import IntegrityError
from django.db.utils import IntegrityError as DjangoIntegrityError

from ..models import Refbook, Version, Element


class RefbookModelTest(TestCase):
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
            version='Тестовая версия1',
            date_start='2023-01-13'
        )
        cls.version2 = Version.objects.create(
            refbook_id=cls.refbook,
            version='Тестовая версия2',
            date_start='2023-03-13'
        )
        cls.element = Element.objects.create(
            version_id=cls.version,
            code='Тестовый код элемента',
            value='Тестовое значение'
        )

    def test_Refbook_model_has_correct_object_name(self):
        """__str__  refbook - это строчка с содержимым refbook.name."""
        text = RefbookModelTest.refbook
        expected_value = text.name
        self.assertEqual(expected_value, str(text))

    def test_Refbook_model_current_version_property(self):
        """Правильно определяется текущая версия справочника."""
        test_version = RefbookModelTest.refbook
        expected_value = test_version.current_version
        self.assertEqual(expected_value, self.version)

    def test_unique_refbook_id_id_version(self):
        """Выдает ошибку при попытке создать версию с именем и id справочника,
        которое уже есть в базе."""
        data = dict(
            refbook_id=self.refbook,
            version='Тестовая версия1',
            date_start='2023-01-23'
        )
        version3 = Version(**data)
        with self.assertRaises((IntegrityError, DjangoIntegrityError)):
            version3.save()

    def test_Version_model_has_correct_object_name(self):
        """__str__  version - это строчка с содержимым
        {version.version} справочника '{version.refbook_id}'."""
        text = RefbookModelTest.version
        expected_value = f"{text.version} справочника '{text.refbook_id}'"
        self.assertEqual(expected_value, str(text))

    def test_Element_model_has_correct_object_name(self):
        """__str__  element - это строчка с содержимым element.value."""
        text = RefbookModelTest.element
        expected_value = text.value
        self.assertEqual(expected_value, str(text))
