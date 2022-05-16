import django_filters
from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductFilter(FilterSet):
    products = CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(products__title__icontains=value) |
                               Q(products__description__icontains=value)
                               ).distinct()

    class Meta:
        model = Stock
        fields = ['products']


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['products']
    filter_class = ProductFilter
