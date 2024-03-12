from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)
    image = models.CharField(max_length=200)

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category_products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_products")
    stock = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.name


class Firm(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "firm"
        verbose_name_plural = "firms"

    def __str__(self):
        return self.name


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_purchases")
    firm = models.ForeignKey(Firm, on_delete=models.PROTECT, related_name="firm_purchases")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brand_purchases")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_purchases")
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_total = models.DecimalField(max_digits=10, decimal_places=2, default=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "purchase"
        verbose_name_plural = "purchases"

    def __str__(self):
        return f"{self.product} - {self.firm} - {self.quantity} - {self.price}"


class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sales")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_sales")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brand_sales")
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_total = models.DecimalField(max_digits=10, decimal_places=2, default=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "sales"
        verbose_name_plural = "saleses"

    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.price}"


    
