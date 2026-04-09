from django.core.management.base import BaseCommand
from week4.scripts.seed import seed_categories

class Command(BaseCommand):
    help = "Seed default categories for week4"

    def handle(self, *args, **options):
        self.stdout.write("Seeding categories...")
        try:
            seed_categories()
            self.stdout.write(self.style.SUCCESS("Seeding done."))
        except Exception as exc:
            self.stderr.write(str(exc))
            raise
