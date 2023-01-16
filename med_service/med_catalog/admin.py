from django.contrib import admin

from med_catalog.models import Refbook, Version, Element


admin.site.site_title = "Refbook_API"
admin.site.site_header = "Административная панель"
admin.site.index_title = "Сервис терминологии"


class VersionAdmin(admin.TabularInline):
    model = Version
    extra = 0


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'current_version',
        'current_version_date'
    )
    inlines = [VersionAdmin]

    def current_version(self, obj):
        return obj.current_version

    def current_version_date(self, obj):
        current_v = obj.current_version
        if current_v is None:
            return None
        return current_v.date_start

    current_version.short_description = "Текущая версия"
    current_version_date.short_description = "Дата начала действия версии"


class ElementAdmin(admin.TabularInline):
    model = Element
    extra = 0


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('refbook_pk', 'refbook_id', 'version', 'date_start')
    inlines = [ElementAdmin]

    def refbook_pk(self, obj):
        return obj.refbook_id.pk

    refbook_pk.short_description = "Код справочника"


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('version_id', 'code', 'value')
