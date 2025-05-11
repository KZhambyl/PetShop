from django.urls import path
from . import views


urlpatterns = [
    path('pets/', views.pet_category_list),  # GET/POST all pet categories
    path('pets/<int:id>/', views.pet_category_detail),  # GET/PUT/DELETE one pet category

    path('pets/<int:id>/categories/', views.item_category_list),  # GET/POST categories
    path('pets/<int:id>/categories/<int:cat_id>/', views.item_category_detail),  # GET/PUT/DELETE one item category

    path('pets/<int:id>/categories/<int:cat_id>/items/', views.item_list_by_pet_and_category),  # GET/POST items
    path('pets/<int:id>/categories/<int:cat_id>/items/<int:it_id>/', views.item_detail),  # GET/PUT/DELETE item

    path('pets/<int:id>/categories/<int:cat_id>/items/<int:it_id>/reviews/', views.ReviewListCreateAPIView.as_view()),
    path('pets/<int:id>/categories/<int:cat_id>/items/<int:it_id>/reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view()),
]
