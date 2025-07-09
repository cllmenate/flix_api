from django.db.models import Count
from rest_framework import generics, views, response
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissionClass
from movies.models import Movie
from movies.serializers import MovieSerializer
from reviews.models import Review


# Create your views here.
class MovieListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()

    def get(self, request, *args, **kwargs):
        total_movies = self.queryset.count()
        movies_per_genre = (
            self.queryset.values('genre__name')
            .annotate(count=Count('id'))
            .order_by('genre__name')
        )
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=Count('rating'))['average_rating']

        return response.Response(
            data={
                "message": "Movie statistics",
                "total_movies": total_movies,
                "movies_per_genre": movies_per_genre,
                "total_reviews": total_reviews,
                "average_rating": round(average_rating, 1) if average_rating else 0,
            },
            status=response.status.HTTP_200_OK,
        )