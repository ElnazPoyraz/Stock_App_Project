from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Brand, Product, Firm, Purchases, Sales
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, FirmSerializer, PurchasesSerializer, SalesSerializer, CategorySearchSerializer, ProductUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status



class CategoryMVS(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
        if 'search' in self.request.query_params:
            return CategorySearchSerializer
        return super().get_serializer_class()


class BrandMVS(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductMVS(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
      
        if self.request.method == "PUT":
            return ProductUpdateSerializer
        return ProductSerializer


class FirmMVS(ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


class PurchasesMVS(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['firm', 'product']
    search_fields = ['firm']
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
                
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        product = Product.objects.get(id=product_id)

        if product.stock == None :
           product.stock = 0

        product.stock += quantity
        product.save()

        self.perform_create(serializer)
        
        return Response(serializer.data)


        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        old_quantity = instance.quantity
        product_id = instance.product.id
        
        new_quantity = request.data.get('quantity')
        
        product = Product.objects.get(id=product_id)

        product.stock -= old_quantity
        product.stock += new_quantity

        product.save()

        self.perform_update(serializer)

        return Response(serializer.data)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        quantity = instance.quantity
        product = instance.product

        product.stock -= quantity
        product.save()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SalesMVS(ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['brand', 'product']
    search_fields = ['brand']


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
                
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        product = Product.objects.get(id=product_id)

        if product.stock == None :
           product.stock = 0

        if product.stock >= quantity:
            product.stock -= quantity
            product.save()

            self.perform_create(serializer)
            return Response(serializer.data)

        return Response("stock yeterli değil!! lütfen geçerli bir quantity miktarı giriniz...")


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        old_quantity = instance.quantity
        product_id = instance.product.id
        
        new_quantity = request.data.get('quantity')
        
        product = Product.objects.get(id=product_id)

        
        product.stock += old_quantity
        product.stock -= new_quantity

        product.save()

        self.perform_update(serializer)

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        quantity = instance.quantity
        product = instance.product

        product.stock += quantity
        product.save()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
