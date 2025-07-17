import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from movies.models import Movie
from genres.models import Genre
from actors.models import Actor


class Command(BaseCommand):
    help = 'Import movies from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing movie data')

    def handle(self, **options):
        file_path = options['file_path']
        self.stdout.write(f'Importing movies from {file_path}...')
        # Logic to read the CSV file and import movies would go here
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get('title')
                    genre_name = row.get('genre')
                    description = row.get('description', '')
                    release_date = datetime.strptime(row.get('release_date'), '%Y-%m-%d').date() if row.get('release_date') else None
                    duration = int(row.get('duration', 0))
                    actor_names = [name.strip() for name in row.get('actors', '').split(';') if name.strip()]
                    self.stdout.write(f'Processing: {row}')

                    self.stdout.write(self.style.NOTICE(f'Processing movie: {title}'))

                    # Buscar instância de Genre
                    try:
                        genre = Genre.objects.get(name=genre_name)
                    except Genre.DoesNotExist:
                        self.stderr.write(f'Error: Genre "{genre_name}" not found for movie "{title}".')
                        continue

                    # Buscar instâncias de Actor
                    actor_objs = []
                    for actor_name in actor_names:
                        try:
                            actor_objs.append(Actor.objects.get(name=actor_name))
                        except Actor.DoesNotExist:
                            self.stderr.write(f'Error: Actor "{actor_name}" not found for movie "{title}".')

                    movie, created = Movie.objects.update_or_create(
                        title=title,
                        defaults={
                            'genre': genre,
                            'description': description,
                            'release_date': release_date,
                            'duration': duration,
                        },
                    )
                    # Adicionar atores (ManyToMany)
                    if actor_objs:
                        movie.actors.set(actor_objs)
        except FileNotFoundError:
            self.stderr.write(f'Error: The file {file_path} does not exist.')
            return
        except Exception as e:
            self.stderr.write(f'Error: {str(e)}')
            return
        self.stdout.write(self.style.SUCCESS('Movies imported successfully!'))
