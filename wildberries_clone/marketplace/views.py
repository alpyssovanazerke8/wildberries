from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import Product, Category, CartItem, Order
from .serializers import (
    UserSerializer, CategorySerializer, ProductModelSerializer,
    CartItemModelSerializer, OrderModelSerializer
)
from .permissions import IsAuthenticatedOrReadOnly


# FBV для аутентификации
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)


# FBV для продуктов
@api_view(['GET'])
def product_list(request):
    """Get list of products with optional filtering"""
    category_slug = request.query_params.get('category')

    if category_slug:
        products = Product.objects.get_products_by_category(category_slug)
    else:
        products = Product.objects.get_available_products()

    serializer = ProductModelSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail(request, pk=None):
    """Full CRUD for products"""
    if request.method == 'GET':
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductModelSerializer(product)
        else:
            products = Product.objects.all()
            serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductModelSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV для категорий
class CategoryList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV для корзины (CRUD)
class CartItemList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemModelSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Проверяем, есть ли уже такой товар в корзине
            product_id = serializer.validated_data['product_id']
            try:
                cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
                # Если есть, увеличиваем количество
                cart_item.quantity += serializer.validated_data['quantity']
                cart_item.save()
                result_serializer = CartItemModelSerializer(cart_item)
                return Response(result_serializer.data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                # Если нет, создаем новый
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(CartItem, pk=pk, user=user)

    def get(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemModelSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemModelSerializer(cart_item, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        serializer = CartItemModelSerializer(cart_item, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = self.get_object(pk, request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV для заказов
class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderModelSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Order, pk=pk, user=user)

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        serializer = OrderModelSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk, request.user)
        serializer = OrderModelSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        order = self.get_object(pk, request.user)
        serializer = OrderModelSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk, request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD для продуктов
class ProductList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductModelSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductModelSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)