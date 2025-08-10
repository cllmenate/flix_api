from django.db.models import Count, Avg
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissionClass
from movies.models import Movie
from movies.serializers import MovieSerializer, MovieListDetailSerializer, MovieStatsSerializer
from reviews.models import Review


# Create your views here.
class MovieListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieSerializer


class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermissionClass,)
    queryset = Movie.objects.all()

    def get(self, request):
        total_movies = self.queryset.count()
        movies_per_genre = (
            self.queryset.values('genre__name')
            .annotate(count=Count('id'))
            .order_by('genre__name')
        )
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']

        data = {
            "message": "Movie statistics",
            "total_movies": total_movies,
            "movies_per_genre": movies_per_genre,
            "total_reviews": total_reviews,
            "average_rating": round(average_rating, 1) if average_rating else 0.0,
        }

        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )
