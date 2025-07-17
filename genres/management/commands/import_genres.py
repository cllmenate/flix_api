import csv
from django.core.management.base import BaseCommand
from genres.models import Genre


class Command(BaseCommand):
    help = 'Import genres from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing genre data')

    def handle(self, **options):
        file_path = options['file_path']
        self.stdout.write(f'Importing genres from {file_path}...')
        # Logic to read the CSV file and import genres would go here
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row.get('name')
                    description = row.get('description')
                    self.stdout.write(f'Processing: {row}')

                    self.stdout.write(self.style.NOTICE(f'Processing genre: {name}'))

                    Genre.objects.update_or_create(
                        name=name,
                        defaults={
                            'description': description
                        },
                    )
        except FileNotFoundError:
            self.stderr.write(f'Error: The file {file_path} does not exist.')
            return
        except Exception as e:
            self.stderr.write(f'Error: {str(e)}')
            return
        self.stdout.write(self.style.SUCCESS('Genres imported successfully!'))
