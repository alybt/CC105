
import pandas as pd
import json
import re
import os
from django.conf import settings
from predictor.models import Game
from datetime import datetime

class CSVDataSync:
    """Handle CSV to Database and Database to CSV synchronization"""
    
    def __init__(self, csv_path='games.csv'):
        self.csv_path = os.path.join(settings.BASE_DIR, csv_path)
    
    def import_csv_to_db(self, verbose=True):
        """Import all games from CSV to Database"""
        
        if not os.path.exists(self.csv_path):
            if verbose:
                print(f"❌ CSV file not found: {self.csv_path}")
            return {'status': 'error', 'message': 'CSV file not found'}
        
        if verbose:
            print(f"📥 Importing from {self.csv_path}...")
        df = pd.read_csv(self.csv_path, index_col=0)
        def clean_k_values(value):
            if pd.isna(value):
                return 0
            if isinstance(value, str):
                if 'K' in value.upper():
                    try:
                        return int(float(value.upper().replace('K', '')) * 1000)
                    except:
                        return 0
            try:
                return int(float(value))
            except:
                return 0
        
        numeric_cols = ['Times Listed', 'Number of Reviews', 'Plays', 'Playing', 'Backlogs', 'Wishlist']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].apply(clean_k_values)
        def extract_year(date_str):
            if pd.isna(date_str):
                return None
            match = re.search(r'\d{4}', str(date_str))
            return int(match.group()) if match else None
        
        if 'Release Date' in df.columns:
            df['release_year'] = df['Release Date'].apply(extract_year)
        def parse_genre(genres_str):
            if pd.isna(genres_str):
                return 'Unknown'
            try:
                genres = eval(genres_str) if isinstance(genres_str, str) else genres_str
                if isinstance(genres, list) and len(genres) > 0:
                    return genres[0]
                return 'Unknown'
            except:
                return 'Unknown'
        
        if 'Genres' in df.columns:
            df['genre'] = df['Genres'].apply(parse_genre)
        games_created = 0
        games_updated = 0
        
        for idx, row in df.iterrows():
            title = row.get('Title', f'Game_{idx}')
            game, created = Game.objects.update_or_create(
                name=title,
                defaults={
                    'release_year': row.get('release_year', 2020),
                    'genre': row.get('genre', 'Unknown'),
                    'description': row.get('Summary', '')[:500],
                    'times_listed': row.get('Times Listed', 0),
                    'num_reviews': row.get('Number of Reviews', 0),
                    'plays': row.get('Plays', 0),
                    'playing': row.get('Playing', 0),
                    'backlogs': row.get('Backlogs', 0),
                    'wishlist': row.get('Wishlist', 0),
                    'rating': row.get('Rating', None),
                }
            )
            
            if created:
                games_created += 1
            else:
                games_updated += 1
            
            if verbose and (games_created + games_updated) % 100 == 0:
                print(f"   Processed {games_created + games_updated} games...")
        
        if verbose:
            print(f"\n✅ Import complete!")
            print(f"   New games: {games_created}")
            print(f"   Updated games: {games_updated}")
            print(f"   Total games: {Game.objects.count()}")
        
        return {
            'status': 'success',
            'created': games_created,
            'updated': games_updated,
            'total': Game.objects.count()
        }
    
    def export_db_to_csv(self, verbose=True):
        """Export all games from Database to CSV"""
        
        if verbose:
            print(f"📤 Exporting to {self.csv_path}...")
        
        games = Game.objects.all()
        
        data = []
        for game in games:
            data.append({
                'Title': game.name,
                'Release Date': f'Jan 01, {game.release_year}' if game.release_year else '',
                'Team': '[]',
                'Rating': game.rating if game.rating else '',
                'Times Listed': game.times_listed,
                'Number of Reviews': game.num_reviews,
                'Genres': f"['{game.genre}']",
                'Summary': game.description,
                'Reviews': '[]',
                'Plays': game.plays,
                'Playing': game.playing,
                'Backlogs': game.backlogs,
                'Wishlist': game.wishlist,
            })
        
        df = pd.DataFrame(data)
        for col in ['Times Listed', 'Number of Reviews', 'Plays', 'Playing', 'Backlogs', 'Wishlist']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f"{x//1000}K" if x >= 1000 else str(x))
        
        df.to_csv(self.csv_path, index=True)
        
        if verbose:
            print(f"✅ Exported {len(data)} games to {self.csv_path}")
        
        return {
            'status': 'success',
            'exported': len(data),
            'file': self.csv_path
        }
    
    def sync_from_csv(self, verbose=True):
        """Sync database from CSV (CSV is source of truth)"""
        return self.import_csv_to_db(verbose)
    
    def sync_from_db(self, verbose=True):
        """Sync CSV from database (Database is source of truth)"""
        return self.export_db_to_csv(verbose)
sync_service = CSVDataSync()