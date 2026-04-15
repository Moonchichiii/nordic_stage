from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seeds the database with initial development data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Database seeding started...'))

        # We will add actual model creation logic here later once we build out
        # the domain models (Events, Speakers, etc.) in the Backend track.

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database!')
        )
