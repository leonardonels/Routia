from django.urls import path
from . import views

app_name = "maps"

urlpatterns = [
    path('planner/', views.planner, name='planner'),
    path('planner/save_route/', views.save_route, name='save_route'),
    path('tour/', views.tour_view, name='tour'),
    path('tour/filter/', views.filter_view, name='filter'),
    path('planner/<int:route_id>/', views.planner, name='planner'),
]
