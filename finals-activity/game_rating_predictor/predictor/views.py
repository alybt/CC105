
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django import forms
from django.core.management import call_command
from .models import Game, PredictionHistory
import joblib
import pickle
import os
import numpy as np
from django.conf import settings
from .services.sync_service import sync_service
class RatingPredictor:
    """Load and use the trained model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = None
        self.load_model()
    
    def load_model(self):
        """Load trained model files"""
        model_dir = os.path.join(settings.BASE_DIR, 'model_files')
        
        model_path = os.path.join(model_dir, 'best_model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        features_path = os.path.join(model_dir, 'features.pkl')
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                if os.path.exists(scaler_path):
                    self.scaler = joblib.load(scaler_path)
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                print(f"Model loaded with {len(self.features)} features")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
        return False
    
    def predict(self, form_data):
        """Make prediction using trained model"""
        
        if self.model and self.features:
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
            
            rating = float(self.model.predict(X)[0])
            return rating
        else:
            return self._fallback_prediction(form_data)
    
    def _fallback_prediction(self, form_data):
        """Simple calculation when model isn't available"""
        times_listed = int(form_data.get('times_listed', 0))
        num_reviews = int(form_data.get('num_reviews', 0))
        plays = int(form_data.get('plays', 0))
        
        score = (times_listed / 10000 + num_reviews / 10000 + plays / 50000) / 3
        rating = 3.0 + score * 1.5
        
        genre = form_data.get('genre', '').lower()
        if genre in ['adventure', 'rpg', 'action']:
            rating += 0.3
        
        return min(5.0, max(1.0, rating))
predictor = RatingPredictor()
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'release_year', 'genre', 'description', 'times_listed', 
                    'num_reviews', 'plays', 'playing', 'backlogs', 'wishlist']
def game_list(request):
    games = Game.objects.all().order_by('-created_at')
    return render(request, 'predictor/game_list.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    prediction = predictor.predict({
        'times_listed': game.times_listed,
        'num_reviews': game.num_reviews,
        'plays': game.plays,
        'playing': game.playing,
        'backlogs': game.backlogs,
        'wishlist': game.wishlist,
        'release_year': game.release_year,
        'genre': game.genre,
    })
    return render(request, 'predictor/game_detail.html', {
        'game': game,
        'predicted_rating': round(prediction, 2)
    })

def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'predictor/game_form.html', {'form': form, 'action': 'Add'})

def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    else:
        form = GameForm(instance=game)
    return render(request, 'predictor/game_form.html', {'form': form, 'action': 'Edit'})

def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('game_list')
    return render(request, 'predictor/game_confirm_delete.html', {'game': game})
def home(request):
    """Home page with prediction form"""
    context = {
        'title': 'Game Rating Predictor',
        'description': 'Enter game details below to predict its rating',
        'model_ready': predictor.model is not None,
        'genres': ['Adventure', 'RPG', 'Action', 'Indie', 'Platform', 'Puzzle', 'Strategy', 'Shooter']
    }
    return render(request, 'predictor/home.html', context)

def predict(request):
    """Handle prediction request with REAL ML model"""
    if request.method == 'POST':
        try:
            game_name = request.POST.get('game_name', 'Unknown Game')
            times_listed = request.POST.get('times_listed', 0)
            num_reviews = request.POST.get('num_reviews', 0)
            plays = request.POST.get('plays', 0)
            playing = request.POST.get('playing', 0)
            backlogs = request.POST.get('backlogs', 0)
            wishlist = request.POST.get('wishlist', 0)
            release_year = request.POST.get('release_year', 2020)
            genre = request.POST.get('genre', 'Unknown')
            review_text = request.POST.get('review_text', '')
            form_data = {
                'times_listed': times_listed,
                'num_reviews': num_reviews,
                'plays': plays,
                'playing': playing,
                'backlogs': backlogs,
                'wishlist': wishlist,
                'release_year': release_year,
                'genre': genre,
            }
            rating = predictor.predict(form_data)
            PredictionHistory.objects.create(
                game_name=game_name[:200],
                predicted_rating=rating,
                times_listed=int(times_listed),
                num_reviews=int(num_reviews),
                plays=int(plays),
                playing=int(playing),
                backlogs=int(backlogs),
                wishlist=int(wishlist),
                release_year=int(release_year),
                genre=genre,
                review_text=review_text[:500]
            )
            if rating >= 4.0:
                category = 'High Rated'
                color = 'success'
                recommendation = 'Excellent game! Highly recommended.'
            elif rating >= 3.0:
                category = 'Average Rated'
                color = 'warning'
                recommendation = ' Decent game. Worth a try.'
            else:
                category = 'Low Rated'
                color = 'danger'
                recommendation = ' Needs improvement. Not recommended.'

            result = {
                'rating': round(rating, 2),
                'category': category,
                'color': color,
                'recommendation': recommendation,
                'error': None,
                'model_used': predictor.model is not None
            }
            return render(request, 'predictor/result.html', {'result': result, 'review_text': review_text[:200]})
            
        except Exception as e:
            result = {'error': str(e)}
            return render(request, 'predictor/result.html', {'result': result})

    return redirect('home')
def prediction_history(request):
    """View all past predictions"""
    predictions = PredictionHistory.objects.all().order_by('-created_at')
    return render(request, 'predictor/prediction_history.html', {'predictions': predictions})
def batch_predict(request):
    """Predict ratings for all games in database"""
    if request.method == 'POST':
        games = Game.objects.all()
        predictions = []
        
        for game in games:
            rating = predictor.predict({
                'times_listed': game.times_listed,
                'num_reviews': game.num_reviews,
                'plays': game.plays,
                'playing': game.playing,
                'backlogs': game.backlogs,
                'wishlist': game.wishlist,
                'release_year': game.release_year,
                'genre': game.genre,
            })
            predictions.append({
                'game': game,
                'predicted_rating': round(rating, 2)
            })
        
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        
        return render(request, 'predictor/batch_predictions.html', {'predictions': predictions})
    
    return redirect('game_list')
def train_model(request):
    """Trigger model training from browser"""
    if request.method == 'POST':
        try:
            call_command('train_model')
            predictor.load_model()
            return JsonResponse({'status': 'success', 'message': 'Model trained and loaded!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'error': 'POST method required'}, status=400)
def import_csv_view(request):
    """Import CSV to database"""
    if request.method == 'POST':
        result = sync_service.import_csv_to_db()
        return JsonResponse(result)
    
    return render(request, 'predictor/import_csv.html')

def export_csv_view(request):
    """Export database to CSV"""
    if request.method == 'POST':
        result = sync_service.export_db_to_csv()
        return JsonResponse(result)
    
    return render(request, 'predictor/export_csv.html')

def sync_status(request):
    """Check sync status"""
    return JsonResponse({
        'csv_exists': os.path.exists(sync_service.csv_path),
        'csv_path': sync_service.csv_path,
        'games_in_db': Game.objects.count(),
    })
def test(request):
    """Simple test view to check if Django is working"""
    return HttpResponse(" Django is working! Test successful.")