from django.urls import path
from . import views

urlpatterns = [
    # Add your actor-related URL patterns here
    path('actors/', 
         views.ActorCreateListView.as_view(), 
         name = 'actor-create-list-view'),
    path('actors/<int:pk>/', 
         views.ActorRetrieveUpdateDestroyView.as_view(), 
         name = 'actor-detail-view'),
]