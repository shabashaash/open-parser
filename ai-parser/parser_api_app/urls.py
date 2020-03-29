from django.urls import path
from .views import tagsView,labelsView,zerosView,Parse,Trainer
urlpatterns = [
    path('tags/', tagsView.as_view()),
    path('labels/', labelsView.as_view()),
    path('zeros/', zerosView.as_view()),
    path('parse/', Parse.as_view()),
    path('trainer/', Trainer.as_view()),
]