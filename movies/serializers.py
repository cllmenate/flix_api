from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('rating'))['rating__avg']

        if rate:
            return round(rate, 1)
        
        return None

    def validate_description(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Description must be 500 characters or less.")
        return value