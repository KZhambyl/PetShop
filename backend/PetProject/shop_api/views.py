from django.shortcuts import render
from .models import Item, ItemCategory, PetCategory, Review
from .serializers import PetCategorySerializer, ItemCategorySerializer, ItemSerializer, ReviewSerializer, RegistrationSerializer
from .permissions import IsOwnerOrAdminOrReadOnly, IsOwnerOrReadOnly, AdminOrReadOnly
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import permissions

# Create your views here.

# Pet category

@api_view(['GET', 'POST'])
def pet_category_list(request):
    if request.method == 'GET':
        pets = PetCategory.objects.all()
        serializer = PetCategorySerializer(pets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PetCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pet_category_detail(request, id):
    pet = get_object_or_404(PetCategory, pk=id)

    if request.method == 'GET':
        serializer = PetCategorySerializer(pet)
        return Response(serializer.data)

    if not request.user.is_staff:
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = PetCategorySerializer(instance=pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Item category

@api_view(['GET','POST'])
def item_category_list(request, id):
    if request.method == 'GET':
        categories = ItemCategory.objects.all()
        serializer = ItemCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ItemCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def item_category_detail(request, id, cat_id):
    category = get_object_or_404(ItemCategory, pk=cat_id)

    if request.method == 'GET':
        serializer = ItemCategorySerializer(category)
        return Response(serializer.data)

    if not request.user.is_staff:
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ItemCategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Item

@api_view(['GET', 'POST'])
@permission_classes([AdminOrReadOnly])
def item_list_by_pet_and_category(request, id, cat_id):
    if request.method == 'GET':
        items = Item.objects.filter(pet_category_id=id, item_category_id=cat_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['pet_category'] = id
        data['item_category'] = cat_id
        
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AdminOrReadOnly])
def item_detail(request, id, cat_id, it_id):
    item = get_object_or_404(Item, pk=it_id, pet_category_id=id, item_category_id=cat_id)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ItemSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Review

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(item_id=self.kwargs['it_id'])

    def perform_create(self, serializer):
        item = generics.get_object_or_404(Item, id=self.kwargs['it_id'])
        serializer.save(user=self.request.user, item=item)


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(item_id=self.kwargs['it_id'])
    
# Authentication

class RegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)