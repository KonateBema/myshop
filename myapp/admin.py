from django.contrib import admin
from .models import (
    Category,
    Supplier,
    SupplierDetail,
    Product,
    HomePage,
    Commande,
    HomeSlide,
    Slide,
    Order
)

# ========== Category ==========
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# ========== Supplier ==========
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')


# ========== Supplier Detail ==========
@admin.register(SupplierDetail)
class SupplierDetailAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'country', 'supplier_type')


# ========== Product ==========
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'quantity',
        'stock_status',
        'categories_list',
        'supplier',
    )
    list_filter = ('categories', 'supplier')
    search_fields = ('name',)
    filter_horizontal = ('categories',)


# ========== Home Page ==========
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('site_name',)


# ========== Commande ==========
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'customer_name',
        'payment',
        'quantity',
        'is_delivered',
        'created_at',
    )
    list_filter = ('payment', 'is_delivered')
    search_fields = ('customer_name', 'customer_phone')


# ========== Home Slide ==========
@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'action_text')


# ========== Slide ==========
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title',)


# ========== Order ==========
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'customer_name',
        'payment',
        'quantity',
        'total_amount',
        'created_at',
    )

