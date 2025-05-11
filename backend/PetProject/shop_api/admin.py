from django.contrib import admin
from .models import ItemCategory, PetCategory, Item, Review

# Register your models here.

admin.site.register(Item)
admin.site.register(ItemCategory)
admin.site.register(PetCategory)
admin.site.register(Review)