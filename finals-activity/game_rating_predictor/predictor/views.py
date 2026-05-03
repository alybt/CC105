from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    context = {
        'title': 'Game Rating Predictor',
        'description': 'Enter game details below to predict its rating'
    }
    return render(request, 'predictor/home.html', context)

def predict(request):
    """Handle prediction request"""
    if request.method == 'POST':
        # Get form data
        times_listed = request.POST.get('times_listed', 0)
        num_reviews = request.POST.get('num_reviews', 0)
        plays = request.POST.get('plays', 0)
        playing = request.POST.get('playing', 0)
        backlogs = request.POST.get('backlogs', 0)
        wishlist = request.POST.get('wishlist', 0)
        release_year = request.POST.get('release_year', 0)
        review_text = request.POST.get('review_text', '')

        # Dummy prediction logic (replace with ML model later)
        try:
            # Simple average for demonstration
            rating = (int(times_listed) + int(num_reviews) + int(plays) + int(playing) + int(backlogs) + int(wishlist)) / 30000 * 5
            rating = max(0, min(5, round(rating, 2)))
        except Exception as e:
            result = {'error': str(e)}
            return render(request, 'predictor/result.html', {'result': result, 'review_text': review_text})

        # Categorize rating
        if rating >= 4.0:
            category = 'High Rated'
            color = 'success'
            recommendation = 'Excellent game! Highly recommended.'
        elif rating >= 3.0:
            category = 'Average Rated'
            color = 'warning'
            recommendation = 'Decent game. Worth a try.'
        else:
            category = 'Low Rated'
            color = 'danger'
            recommendation = 'Needs improvement.'

        result = {
            'rating': rating,
            'category': category,
            'color': color,
            'recommendation': recommendation,
            'error': None
        }
        return render(request, 'predictor/result.html', {'result': result, 'review_text': review_text})
    else:
        # If not POST, redirect to home
        from django.shortcuts import redirect
        return redirect('home')