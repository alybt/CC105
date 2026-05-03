# predictor/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import threading

# Local thread storage to prevent recursion
_thread_local = threading.local()

class Game(models.Model):
    name = models.CharField(max_length=200)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    times_listed = models.IntegerField(default=0)
    num_reviews = models.IntegerField(default=0)
    plays = models.IntegerField(default=0)
    playing = models.IntegerField(default=0)
    backlogs = models.IntegerField(default=0)
    wishlist = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Rating field
    rating = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Actual rating (0-5)"
    )
    
    def __str__(self):
        return self.name
    
    @property
    def is_high_rated(self):
        return self.rating is not None and self.rating >= 4.0


class PredictionHistory(models.Model):
    """Store all predictions made by users"""
    game_name = models.CharField(max_length=200)
    predicted_rating = models.FloatField()
    times_listed = models.IntegerField()
    num_reviews = models.IntegerField()
    plays = models.IntegerField()
    playing = models.IntegerField()
    backlogs = models.IntegerField()
    wishlist = models.IntegerField()
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    review_text = models.TextField(blank=True)
    actual_rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.game_name} - {self.predicted_rating}"


# --- Signals for Auto-Sync ---
@receiver(post_save, sender=Game)
@receiver(post_delete, sender=Game)
def auto_sync_to_csv(sender, **kwargs):
    """Automatically sync to CSV when database changes"""
    
    # Prevent recursion
    if hasattr(_thread_local, 'is_syncing') and _thread_local.is_syncing:
        return
    
    _thread_local.is_syncing = True
    
    try:
        from predictor.services.sync_service import sync_service
        # Export to CSV after any change
        sync_service.export_db_to_csv(verbose=False)
    except Exception as e:
        print(f"Auto-sync error: {e}")
    finally:
        _thread_local.is_syncing = False