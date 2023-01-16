from rest_framework import serializers

from med_catalog.models import Refbook, Element


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = ('id', 'code', 'name',)


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('code', 'value',)
