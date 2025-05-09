from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, Cart, CartItem, Order, OrderItem


# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')


# Register the SubCategory model
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    search_fields = ('name', 'slug', 'category__name')


# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'price', 'stock', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'subcategory__name', 'sku')
    list_filter = ('is_active', 'is_featured', 'subcategory')


# Register the ProductImage model
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_main')
    search_fields = ('product__name',)


# Register the Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)


# Register the CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')


# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'status', 'ordered_at', 'is_paid')
    search_fields = ('user__username', 'payment_id')
    list_filter = ('status', 'is_paid')


# Register the OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_purchase')
    search_fields = ('order__user__username', 'product__name')
