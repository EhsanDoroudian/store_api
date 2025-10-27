from rest_framework import serializers
from django.utils.text import slugify
from django.db import transaction
from decimal import Decimal

from .models import Cart, CartItem, Category, Customer, Order, OrderItem, Product, Comment


class CategorySerializer(serializers.ModelSerializer):
    product_number = serializers.IntegerField(source='products.count', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'product_number', 'top_product']

    def validate(self, data):
        if len(data['title']) < 3:
            raise serializers.ValidationError("Category title length must at least 3 character.")
        return data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory', 'category', 'slug', 'description', 'unit_price_after_tax']
        
    title = serializers.CharField(max_length=255, source='name')
    unit_price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Product):
        return round(product.price * Decimal(1.09), 1)
    
    def validate(self, data):
        if len(data['name']) < 6:
            raise serializers.ValidationError("Error occured")
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body']
    
    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CartProductSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity',]


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
    
    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        
        self.instance = cart_item
        return cart_item
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    product = CartProductSeriallizer()
    item_total = serializers.SerializerMethodField()

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id',]
    
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']
        read_only_fields = ['user']


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source="user.first_name")
    last_name = serializers.CharField(max_length=255, source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]

        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "status", "datetime_created", "items"]

             
class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = OrderCustomerSerializer()

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "datetime_created", "items"]


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError("This cart does not exist")
        
        if CartItem.objects.filter(cart_id=cart_id).count()== 0:
            raise serializers.ValidationError("This cart is empty")

        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            customer = Customer.objects.get(user_id=user_id)

            order = Order()
            order.customer = customer
            order.save()

            cart_items = CartItem.objects.select_related("product").filter(cart_id = cart_id)

            order_items = [
                OrderItem(
                    order = order,
                    product = cart_item.product,
                    price = cart_item.product.price,
                    quantity = cart_item.quantity,
                ) for cart_item in cart_items
            ]
           
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()

            return order
        

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
