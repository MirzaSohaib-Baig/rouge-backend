from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage, Cart, CartItem, Order, OrderItem
from django_rest_authentication.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
