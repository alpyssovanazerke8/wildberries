from rest_framework import serializers
from .models import Product, Category, CartItem, Order
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ProductModelSerializer(serializers.ModelSerializer):
    oldPrice = serializers.SerializerMethodField()
    isDiscounted = serializers.SerializerMethodField()
    isFavorite = serializers.SerializerMethodField()
    rating = serializers.FloatField(default=4.8)  
    reviewsCount = serializers.IntegerField(default=123)  

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'oldPrice', 'isDiscounted', 'isFavorite', 'rating', 'reviewsCount'
        ]

    def get_oldPrice(self, obj):
        if obj.discount > 0:
            return float(obj.price)
        return None

    def get_isDiscounted(self, obj):
        return obj.discount > 0

    def get_isFavorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False

class CartItemModelSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    product = ProductModelSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'full_name', 'address', 'phone', 'status', 'total_price', 'created_at']
        read_only_fields = ['status', 'total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        # Рассчитываем общую сумму заказа из корзины пользователя
        cart_items = CartItem.objects.filter(user=user)
        total_price = sum(item.total_price for item in cart_items)
        validated_data['total_price'] = total_price

        order = Order.objects.create(**validated_data)

        # Очищаем корзину после создания заказа
        cart_items.delete()

        return order