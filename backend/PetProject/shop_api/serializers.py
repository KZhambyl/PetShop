from rest_framework import serializers
from .models import Item, ItemCategory, PetCategory, Review
from django.contrib.auth.models import User

class PetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    item_category = serializers.PrimaryKeyRelatedField(queryset=ItemCategory.objects.all(), required=False)
    pet_category = serializers.PrimaryKeyRelatedField(queryset=PetCategory.objects.all(), required=False)

    class Meta:
        model = Item
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username instead of user ID
    item = serializers.PrimaryKeyRelatedField(read_only=True)  # prevents overriding in request body

    class Meta:
        model = Review
        fields = ['id', 'item', 'user', 'text', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'item', 'created_at', 'updated_at']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password']
        )
        return user