
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),

    path('games/', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/create/', views.game_create, name='game_create'),
    path('game/<int:pk>/edit/', views.game_update, name='game_update'),
    path('game/<int:pk>/delete/', views.game_delete, name='game_delete'),
    
    path('history/', views.prediction_history, name='prediction_history'),
    path('batch-predict/', views.batch_predict, name='batch_predict'),
    path('train-model/', views.train_model, name='train_model'),
    path('sync/import/', views.import_csv_view, name='import_csv'),
    path('sync/export/', views.export_csv_view, name='export_csv'),
    path('sync/status/', views.sync_status, name='sync_status'),
]   