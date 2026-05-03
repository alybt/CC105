import joblib
import pickle
import numpy as np
import os
from django.conf import settings
from predictor.models import PredictionHistory

class RatingPredictor:
    """Service for making predictions"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = None
        self.load_model()
    
    def load_model(self):
        """Load trained model"""
        model_dir = os.path.join(settings.BASE_DIR, 'model_files')
        
        model_path = os.path.join(model_dir, 'best_model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        features_path = os.path.join(model_dir, 'features.pkl')
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                print(f"✅ Model loaded with {len(self.features)} features")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
        
        return False
    
    def predict(self, form_data, game_name="Unknown"):
        """Make prediction from form data"""
        
        
        feature_vector = []
        
        for feature in self.features:
            if feature.startswith('genre_'):
                
                genre_name = feature.replace('genre_', '').replace('_', ' ').title()
                value = 1 if form_data.get('genre', '').lower() == genre_name.lower() else 0
            else:
                
                value = float(form_data.get(feature, 0))
            
            feature_vector.append(value)
        
        
        X = np.array(feature_vector).reshape(1, -1)
        
        if self.scaler:
            X = self.scaler.transform(X)
        
        if self.model:
            rating = float(self.model.predict(X)[0])
        else:
            rating = self._fallback_prediction(form_data)
        
        self._save_history(form_data, rating, game_name)
        
        return rating
    
    def _fallback_prediction(self, form_data):
        """Simple fallback when model isn't available"""
        times_listed = float(form_data.get('times_listed', 0))
        num_reviews = float(form_data.get('num_reviews', 0))
        plays = float(form_data.get('plays', 0))
        
        score = (times_listed / 10000 + num_reviews / 10000 + plays / 50000) / 3
        rating = 3.0 + score * 1.5
        
        genre = form_data.get('genre', '').lower()
        if genre in ['adventure', 'rpg', 'action']:
            rating += 0.3
        
        return min(5.0, max(1.0, rating))
    
    def _save_history(self, form_data, rating, game_name):
        """Save prediction to database (no IP address)"""
        try:
            PredictionHistory.objects.create(
                game_name=game_name[:200],
                predicted_rating=rating,
                times_listed=int(form_data.get('times_listed', 0)),
                num_reviews=int(form_data.get('num_reviews', 0)),
                plays=int(form_data.get('plays', 0)),
                playing=int(form_data.get('playing', 0)),
                backlogs=int(form_data.get('backlogs', 0)),
                wishlist=int(form_data.get('wishlist', 0)),
                release_year=int(form_data.get('release_year', 2020)),
                genre=form_data.get('genre', 'Unknown'),
                review_text=form_data.get('review_text', '')[:500]
            )
        except Exception as e:
            print(f"Error saving history: {e}")

predictor = RatingPredictor()