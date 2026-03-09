import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titanic_project.settings')
django.setup()

from core.models import Passenger 
def safe_int(value, default=None):
    try: 
        return int(float(value))
    except (ValueError, TypeError):
        return default
 
def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def run_import():
    file_path = 'dataset/titanic.csv' 
    Passenger.objects.all().delete()

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        passengers_to_create = []
        
        for row in reader: 
            if not row.get('name'):
                continue

            passengers_to_create.append(
                Passenger( 
                    survived=safe_int(row.get('survived'), 0),
                    pclass=safe_int(row.get('pclass'), 3),
                    name=row.get('name', 'Unknown'),
                    sex=row.get('sex', ''),
                    age=safe_float(row.get('age'), None),
                    sibsp=safe_int(row.get('sibsp'), 0),
                    parch=safe_int(row.get('parch'), 0),
                    ticket=row.get('ticket', ''),
                    fare=safe_float(row.get('fare'), 0.0),
                    cabin=row.get('cabin', ''),
                    embarked=row.get('embarked', ''),
                    boat=row.get('boat', ''),
                    body=safe_int(row.get('body'), None),
                    home_dest=row.get('home.dest', '')
                )
            )
        
        Passenger.objects.bulk_create(passengers_to_create)
    
    print(f"Successfully imported {len(passengers_to_create)} passengers!")

if __name__ == "__main__":
    run_import()