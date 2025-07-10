from django.urls import path
from . import views


urlpatterns = [
    # Add your actor-related URL patterns here
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-create-list-view'),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail-view'),
]
