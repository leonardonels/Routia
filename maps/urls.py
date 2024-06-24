from django.urls import path
from . import views

app_name = "maps"

urlpatterns = [
    path('planner/', views.planner, name='planner'),
]
