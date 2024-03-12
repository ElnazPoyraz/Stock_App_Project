from django.urls import path, include
from rest_framework import routers
from .views import CategoryMVS, BrandMVS, ProductMVS, FirmMVS, PurchasesMVS, SalesMVS


router = routers.DefaultRouter()
router.register("categories", CategoryMVS)
router.register("brands", BrandMVS)
router.register("products", ProductMVS)
router.register("firms", FirmMVS)
router.register("purchases", PurchasesMVS)
router.register("sales", SalesMVS)

urlpatterns = [
    path("", include(router.urls)),

]