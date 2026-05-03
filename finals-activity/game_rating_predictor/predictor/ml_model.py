import joblib
import pickle
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), 'model_files')

class GameRatingPredictor:
    """Singleton class to load and use the trained model"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Load the trained model and required files"""
        try:
            model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
            self.model = joblib.load(model_path)
            
            scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
            self.scaler = joblib.load(scaler_path)
            

            features_path = os.path.join(MODEL_DIR, 'features.pkl')
            with open(features_path, 'rb') as f:
                self.features = pickle.load(f)
            
            self.is_loaded = True
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.is_loaded = False
            self.model = None
            self.scaler = None
            self.features = []
    
    def predict(self, input_data):
        """
        Make prediction based on input data
        
        Args:
            input_data: dict with feature values
            
        Returns:
            dict with prediction results
        """
        if not self.is_loaded:
            return {'error': 'Model not loaded', 'rating': None}
        
        try:
            feature_vector = []
            for feature in self.features:
                value = input_data.get(feature, 0)
                # Handle missing values
                if value is None or value == '':
                    value = 0
                feature_vector.append(float(value))
            
            X = np.array(feature_vector).reshape(1, -1)
            X_scaled = self.scaler.transform(X)
            rating = self.model.predict(X_scaled)[0]
            if rating >= 4.0:
                category = "High Rated"
                recommendation = "Highly Recommended!"
                color = "success"
            elif rating >= 3.0:
                category = "Average Rated"
                recommendation = "Worth Trying"
                color = "warning"
            else:
                category = "Low Rated"
                recommendation = "Not Recommended"
                color = "danger"
            
            return {
                'rating': round(rating, 2),
                'category': category,
                'recommendation': recommendation,
                'color': color,
                'error': None
            }
            
        except Exception as e:
            return {'error': str(e), 'rating': None, 'category': None}

predictor = GameRatingPredictor()