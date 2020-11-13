"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL



class OrganizationQuerySet(models.QuerySet):


    def tree_downwards(self, root_org_id):
        """
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности


        :type root_org_id: int
        """
        child = [self.get(id=root_org_id)]


        def find_child(all=self,find_id=root_org_id,childer=child):

            for i in all:
                if i.parent_id==find_id:
                    childer.append(i)
                    find_child(find_id=i.id)
        find_child()
        return child



    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        TODO: Написать фильтр с помощью ORM или RawSQL запроса или функций Python

        :type child_org_id: int
        """

        parents = [self.get(id=child_org_id)]
        full_list=Organization.objects.all()


        def find_parents(self=self,find_id=child_org_id,parents=parents):
            for i in self:
                if i.id==self.get(id=find_id).parent_id:
                    parents.append(i)
                    find_parents(find_id=i.id)

        find_parents()

        return parents



class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_upwards()

        :rtype: django.db.models.QuerySet
        """

        only_parents=Organization.objects.tree_upwards(child_org_id=self.id)[1:]
        if self.parent_id is None:
            return Organization.objects.filter(id=self.parent_id)
        else:
            return only_parents







    def children(self):
        """
        Возвращает всех детей любого уровня вложенности
        TODO: Написать метод, используя ORM и .tree_downwards()

        :rtype: django.db.models.QuerySet
        """
        only_child = Organization.objects.tree_downwards(root_org_id=self.id)[1:]

        if len(only_child)==0:
            return Organization.objects.filter(parent_id=self.id)
        else:
            return only_child



    def __str__(self):
        return self.name
