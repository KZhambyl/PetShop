from django.db import models
from django.contrib.auth.models import User

class ItemCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class PetCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    pet_category = models.ForeignKey(PetCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.item.name}"
    
