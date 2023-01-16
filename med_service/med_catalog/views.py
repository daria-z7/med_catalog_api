from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import exceptions
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from med_catalog.models import Refbook, Element
from med_catalog.serializers import RefbookSerializer, ElementSerializer


refbook_response = openapi.Response(
    'Описание ответа',
    RefbookSerializer
)
date_param = openapi.Parameter(
    'date',
    openapi.IN_QUERY,
    description='дата(ГГГГ-ММ-ДД)',
    type=openapi.TYPE_STRING
)


@swagger_auto_schema(
    operation_description='Получение списка справочников',
    method='get',
    manual_parameters=[date_param],
    responses={200: refbook_response},
)
@api_view(['GET',])
def get_refbook_versions(request):
    """Возвращает список справочников, при указании даты в запросе возвращает
    только те справочники, в которых имеются версии с Датой начала действия
    раннее или равной указанной.
    """
    refbooks = Refbook.objects.all()
    date = request.query_params.get('date')
    try:
        if date is not None:
            refbooks = refbooks.filter(versions__date_start__lte=date)
    except exceptions.ValidationError:
        return Response(
            {"errors": "Введите дату в формате ГГГГ-ММ-ДД"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RefbookSerializer(
            refbooks,
            many=True
        )
    return Response(
            {"refbooks": serializer.data},
            status=status.HTTP_200_OK
    )


elements_response = openapi.Response(
    'Описание ответа',
    ElementSerializer
)

pk_param = openapi.Parameter(
    'id',
    openapi.IN_PATH,
    description='номер справочника',
    type=openapi.TYPE_INTEGER
)
version_param = openapi.Parameter(
    'version',
    openapi.IN_QUERY,
    description='название версии',
    type=openapi.TYPE_STRING
)


@swagger_auto_schema(
    operation_description='Получение элементов заданного справочника',
    method='get',
    manual_parameters=[version_param, pk_param],
    responses={200: elements_response}
)
@api_view(['GET',])
def get_version_elements(request, id):
    """Возвращает элементы текущей версии справочника, при указании версии
    в запросе возвращает элементы указанной версии.
    """
    version_filter = request.query_params.get('version')

    if version_filter is not None:
        elements = Element.objects.filter(
            version_id__refbook_id__exact=id
        ).filter(
            version_id__version__exact=version_filter
        )
    else:
        refbook = get_object_or_404(Refbook, pk=id)
        if refbook.current_version is None:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elements = Element.objects.filter(
            version_id=refbook.current_version.id
        )

    serializer = ElementSerializer(
            elements,
            many=True
        )
    return Response(
            {"elements": serializer.data},
            status=status.HTTP_200_OK
        )


code_param = openapi.Parameter(
    'code',
    openapi.IN_QUERY,
    description='код элемента',
    type=openapi.TYPE_STRING
)
value_param = openapi.Parameter(
    'value',
    openapi.IN_QUERY,
    description='значение элемента',
    type=openapi.TYPE_STRING
)


@swagger_auto_schema(
    operation_description='Валидация элемента справочника',
    method='get',
    manual_parameters=[code_param, value_param, version_param, pk_param],
    responses={200: elements_response}
)
@api_view(['GET',])
def check_version_elements(request, id):
    """Валидирует элемент по коду и значению (по версии - при указании),
    возвращает элемент, при нахождении.
    """
    param_code = request.query_params.get('code')
    param_value = request.query_params.get('value')
    param_version = request.query_params.get('version')
    if param_code is None or param_value is None:
        return Response(
            {"detail": "Для проверки элемента введите код и значение"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if param_version is not None:
        element = get_object_or_404(
            Element,
            version_id__refbook_id__exact=id,
            version_id__version__exact=param_version,
            code=param_code,
            value=param_value
        )
    else:
        refbook = get_object_or_404(Refbook, pk=id)
        if refbook.current_version is None:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        element = get_object_or_404(
            Element,
            version_id=refbook.current_version.id,
            code=param_code,
            value=param_value
        )

    serializer = ElementSerializer(element)
    return Response(
            {"element": serializer.data},
            status=status.HTTP_200_OK
        )
