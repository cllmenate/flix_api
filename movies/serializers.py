from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie
from actors.serializers import ActorSerializer
from genres.serializers import GenreSerializer


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_description(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Description must be 500 characters or less.")
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'description', 'release_date', 'duration', 'rate', 'actors',]

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('rating'))['rating__avg']

        if rate:
            return round(rate, 1)

        return None


class MovieStatsSerializer(serializers.Serializer):
    total_movies = serializers.IntegerField()
    movies_per_genre = serializers.ListField()
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
