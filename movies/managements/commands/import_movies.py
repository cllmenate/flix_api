import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Import movies from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing movie data')

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.stdout.write(f'Importing movies from {file_path}...')
        # Logic to read the CSV file and import movies would go here
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row.get('title')
                    genre = row.get('genre')
                    description = row.get('description', '')
                    release_date = datetime.strptime(row.get('release_date'), '%Y-%m-%d').date() if row.get('release_date') else None
                    actors = row.get('actors', '').split(';') if row.get('actors') else []
                    self.stdout.write(f'Processing: {row}')

                    self.stdout.write(self.style.NOTICE(f'Processing movie: {title}'))

                    Movie.objects.update_or_create(
                        title=title,
                        defaults={
                            'genre': genre,
                            'description': description,
                            'release_date': release_date,
                            'duration': int(row.get('duration', 0)),
                            'actors': actors
                        },
                    )
        except FileNotFoundError:
            self.stderr.write(f'Error: The file {file_path} does not exist.')
            return
        except Exception as e:
            self.stderr.write(f'Error: {str(e)}')
            return
        self.stdout.write(self.style.SUCCESS('Movies imported successfully!'))
