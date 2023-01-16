from datetime import datetime

from django.db import models


class Refbook(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='Идентификатор'
    )
    code = models.CharField(
        verbose_name='Код',
        max_length=100,
        unique=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=300,
    )
    description = models.TextField(
        verbose_name='Описание справочника',
        null=True,
        blank=True,
    )

    @property
    def current_version(self):
        try:
            current_v = self.versions.filter(
                date_start__lte=datetime.now()
            ).order_by('-pk')[0]
        except IndexError:
            return None
        return current_v

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return self.name


class Version(models.Model):
    refbook_id = models.ForeignKey(
        Refbook,
        verbose_name='Наименование справочника',
        on_delete=models.CASCADE,
        related_name='versions',
    )
    version = models.CharField(
        verbose_name='Версия',
        max_length=50,
    )
    date_start = models.DateField(
        verbose_name='Дата начала версии',
    )

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'
        constraints = [
            models.UniqueConstraint(
                fields=['refbook_id_id', 'version'],
                name='unique_refbook_id_id_version'
            ),
            models.UniqueConstraint(
                fields=['refbook_id', 'version', 'date_start'],
                name='unique_refbook_id_version_date_start'
            ),
        ]

    def __str__(self):
        return f"{self.version} справочника '{self.refbook_id}'"


class Element(models.Model):
    version_id = models.ForeignKey(
        Version,
        verbose_name='Справочник-версия',
        on_delete=models.CASCADE,
        related_name='elements',
    )
    code = models.CharField(
        verbose_name='Код элемента',
        max_length=100,
    )
    value = models.CharField(
        verbose_name='Значение элемента',
        max_length=300,
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        constraints = [
            models.UniqueConstraint(
                fields=['version_id', 'code', 'value'],
                name='unique_version_id_code_value'
            ),
        ]

    def __str__(self):
        return self.value
