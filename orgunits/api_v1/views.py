"""
Copyright 2020 ООО «Верме»
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import TokenAuthMixin


class OrganizationViewSet(TokenAuthMixin, ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, *args, **kwargs):
        """
        Возвращает родителей запрашиваемой организации
        TODO: Написать два действия для ViewSet (parents и children), используя методы модели
        """

        find=Organization.objects.get(name=self.get_object())
        parents_list=Organization.parents(find)
        serializer = self.get_serializer( parents_list, many=True)

        return Response (serializer.data)

    @action(methods=["GET"], detail=True)
    def children(self, request, *args, **kwargs):
        """
        Возвращает родителей запрашиваемой организации
        TODO: Написать два действия для ViewSet (parents и children), используя методы модели
        """

        find = Organization.objects.get(name=self.get_object())
        children_list = Organization.children(find)
        serializer = self.get_serializer(children_list, many=True)

        return Response(serializer.data)
