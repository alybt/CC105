
from django.core.management.base import BaseCommand
from predictor.services.sync_service import sync_service

class Command(BaseCommand):
    help = 'Export games from database to CSV'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='games.csv',
            help='Path to CSV file'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Exporting games to CSV...'))
        
        if options['csv_file'] != 'games.csv':
            sync_service.csv_path = options['csv_file']
        
        result = sync_service.export_db_to_csv()
        
        if result['status'] == 'success':
            self.stdout.write(self.style.SUCCESS(
                f"Exported {result['exported']} games to {result['file']}"
            ))
        else:
            self.stdout.write(self.style.ERROR(f" Error: {result['message']}"))