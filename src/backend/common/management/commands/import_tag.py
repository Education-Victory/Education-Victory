import json
import os
from django.core.management.base import BaseCommand
from question.models import Tag  # Ensure this is the correct import path

class Command(BaseCommand):
    help = 'Imports default tags into the database'

    def add_arguments(self, parser):
        parser.add_argument('data_file', type=str, help='The JSON file with the default tags')

    def handle(self, *args, **options):
        data_file_path = options['data_file']

        if not os.path.isfile(data_file_path):
            self.stdout.write(self.style.ERROR(f'File does not exist: {data_file_path}'))
            return

        # Load data from JSON file
        with open(data_file_path, 'r') as file:
            data = json.load(file)

        for category_name, tags in data.items():
            for tag_info in tags:
                # Extracting details for each tag
                name = tag_info['name']
                group = tag_info['group']
                short_name = tag_info['short_name']
                frequency = tag_info.get('frequency', 1)
                difficulty = tag_info.get('difficulty', 1)

                # Creating or updating the tag
                tag, created = Tag.objects.update_or_create(
                    name=name,
                    defaults={
                        'short_name': short_name,
                        'group': group,
                        'category': category_name,
                        'frequency': frequency,
                        'difficulty': difficulty
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added tag "{name}"'))
                else:
                    self.stdout.write(f'Tag "{name}" already exists and was updated.')

