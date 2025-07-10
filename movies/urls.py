from django.urls import path
from . import views


urlpatterns = [
    # Add your actor-related URL patterns here
    path('movies/', views.MovieListCreateView.as_view(), name='movie-create-list-view'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyView.as_view(), name='movie-detail-view'),
    path('movies/stats/', views.MovieStatsView.as_view(), name='movie-stats-view'),
]
