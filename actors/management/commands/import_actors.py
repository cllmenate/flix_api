import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from actors.models import Actor


class Command(BaseCommand):
    help = 'Import actors from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing actor data')

    def handle(self, **options):
        file_path = options['file_path']
        self.stdout.write(f'Importing actors from {file_path}...')
        # Logic to read the CSV file and import actors would go here
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row.get('name')
                    date_of_birth = datetime.strptime(row.get('date_of_birth'), '%Y-%m-%d').date() if row.get('date_of_birth') else None
                    nationality = row.get('nationality')
                    biography = row.get('biography')
                    self.stdout.write(f'Processing: {row}')

                    self.stdout.write(self.style.NOTICE(f'Processing actor: {name}'))

                    Actor.objects.update_or_create(
                        name=name,
                        defaults={
                            'date_of_birth': date_of_birth,
                            'nationality': nationality,
                            'biography': biography
                        },
                    )
        except FileNotFoundError:
            self.stderr.write(f'Error: The file {file_path} does not exist.')
            return
        except Exception as e:
            self.stderr.write(f'Error: {str(e)}')
            return
        self.stdout.write(self.style.SUCCESS('Actors imported successfully!'))
