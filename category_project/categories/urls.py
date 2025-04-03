from django.urls import path
from .views import category_list, manage_subcategories

urlpatterns = [
    path('', category_list, name='category-list'),
    path('get-subcategories/', manage_subcategories, name='get-subcategories'),
]
