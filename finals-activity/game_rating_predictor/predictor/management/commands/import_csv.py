
from django.core.management.base import BaseCommand
from predictor.services.sync_service import sync_service

class Command(BaseCommand):
    help = 'Import games from CSV to database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='games.csv',
            help='Path to CSV file'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing games from CSV...'))
        if options['csv_file'] != 'games.csv':
            sync_service.csv_path = options['csv_file']
        
        result = sync_service.import_csv_to_db()
        
        if result['status'] == 'success':
            self.stdout.write(self.style.SUCCESS(
                f"Imported {result['created']} new games, "
                f"updated {result['updated']} existing games"
            ))
        else:
            self.stdout.write(self.style.ERROR(f"Error: {result['message']}"))