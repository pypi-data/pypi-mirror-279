

from django.db.models import Model, QuerySet


class QuerySetManager:
    model: Model


    @classmethod
    def get_queryset(cls, info, **kwargs) -> QuerySet:
        return cls.model.objects.all()
    

    class Meta:
        abstract = True
        

class NodeQuerySetMixin:
    queryset_manager: QuerySetManager

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return cls.queryset_manager.get_queryset(info, **kwargs)

    class Meta:
        abstract = True
