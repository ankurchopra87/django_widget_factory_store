from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework import viewsets, generics, filters
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# Create your views here.


class M2MFilter(django_filters.Filter):
    """ Filter to enable filtering on multiple values"""
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qd = {}
            qd[self.name] = v
            qs = qs.filter(**qd)
        return qs


class SKUFilterSet(django_filters.FilterSet):
    """FilterSet for SKU"""
    attributes = M2MFilter(name='attributes')

    class Meta:
        model = SKU
        fields = ('attributes', 'product_id')


class SKUViewSet(viewsets.ModelViewSet):
    """ViewSet for SKU"""
    queryset = SKU.objects.all().select_related(
        'product'
    ).prefetch_related(
        Prefetch(
            'attributes',
            queryset=Attribute.objects.select_related(
                'type'
            ).order_by('type__name')
        )
    ).order_by('number')
    serializer_class = SKUSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = SKUFilterSet
    search_fields = ('attributes__name',)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product"""
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    filter_fields = ('id',)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order"""
    queryset = Order.objects.all().order_by("-created_timestamp")
    serializer_class = OrderSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    """ViewSet for Attribute"""
    queryset = Attribute.objects.all().order_by("name")
    serializer_class = AttributeSerializer
    filter_fields = ('type__id', 'sku_set__product_id')


class AttributeTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for AttributeType"""
    queryset = AttributeType.objects.prefetch_related(
        Prefetch(
            'attribute_set',
            Attribute.objects.select_related('type').order_by('type__name')
        ),
        Prefetch(
            'attribute_set__sku_set', SKU.objects.all().order_by('number'))
    ).order_by("name").distinct()

    serializer_class = AttributeTypeSerializer
    filter_fields = ('attribute_set__sku_set__product_id', )
