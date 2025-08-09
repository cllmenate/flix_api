from django.core.management.base import BaseCommand
from movies.models import Movie
from movies.serializers import MovieListDetailSerializer


class Command(BaseCommand):
    help = "Check the duration of a movie"

    def handle(self, *args, **options):
        m = Movie.objects.get(id=1)
        print(MovieListDetailSerializer(m).data)
        print(m.duration)  # Deve mostrar 109
