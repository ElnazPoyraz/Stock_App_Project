from rest_framework import serializers
from .models import Category, Brand, Product, Firm, Purchases, Sales


class CategorySerializer(serializers.ModelSerializer):
    
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"
        read_only_field = ["id"]


    def get_product_count(self, obj):
        return obj.category_products.count()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        read_only_field = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()

    stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_field = ["id"]


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = "__all__"
        read_only_field = ["id"]


class PurchasesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()

    price_total = serializers.SerializerMethodField()

#    product = ProductSerializer(read_only=True)
    category = serializers.CharField(source='product.category.name', read_only=True)
    category_id = serializers.IntegerField(source='product.category.id', read_only=True)

    class Meta:
        model = Purchases
        fields = [
            "id",
            "user",
            "user_id",
            "firm",
            "firm_id",
            "brand",
            "brand_id",
            "category",
            "category_id",
            "product",
            "product_id",
            "quantity",
            "price",
            "price_total",
            "created",
            "updated",
        ]
        read_only_field = ["id"]


    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        instance = Purchases.objects.create(**validated_data)
        return instance


    def get_price_total(self, obj):
        price_total = obj.price * obj.quantity
        return price_total


class SalesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()

    price_total = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = [
            "id",
            "user",
            "user_id",
            "product",
            "product_id",
            "brand",
            "brand_id",
            "quantity",
            "price",
            "price_total",
            "created",
            "updated",
        ]
        read_only_field = ["id"]


    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        instance = Sales.objects.create(**validated_data)
        return instance


    def get_price_total(self, obj):
        price_total = obj.price * obj.quantity
        return price_total


class CategorySearchSerializer(serializers.ModelSerializer):
    category_products = ProductSerializer(many=True) 

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_products']


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'brand', 'stock', 'product_sales', 'product_purchases']

    def update(self, instance, validated_data):
        sales = validated_data.get('product_sales')
        purchases = validated_data.get('product_purchases')

        instance.sales += sales
        instance.purchases += purchases
        instance.stock += (purchases - sales)
        
        instance.save()
        
        return instance