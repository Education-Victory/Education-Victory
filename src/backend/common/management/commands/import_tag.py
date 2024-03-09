import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from question.models import Tag  # Ensure this is the correct import path

class Command(BaseCommand):
    help = 'Imports default tags into the database'

    def handle(self, *args, **options):
        data_file_path = os.path.join(os.path.dirname(__file__), 'default_tag.json')

        # Load data from JSON file
        with open(data_file_path, 'r') as file:
            data = json.load(file)

        for category, tags in data.items():
            for tag_info in tags:
                # Extracting details for each tag
                name = tag_info['name']
                category = tag_info.get('category', 'General')
                frequency = tag_info.get('frequency', 1)
                difficulty = tag_info.get('difficulty', 1)

                # Creating or updating the tag
                tag, created = Tag.objects.get_or_create(
                    name=name,
                    defaults={
                        'created_at': timezone.now(),
                        'category': category,
                        'frequency': frequency,
                        'difficulty': difficulty
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added tag "{name}"'))
                else:
                    # If the tag exists, you might want to update its fields
                    tag.category = category
                    tag.frequency = frequency
                    tag.difficulty = difficulty
                    tag.save()
                    self.stdout.write(f'Tag "{name}" already exists and was updated.')
