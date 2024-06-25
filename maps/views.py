from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Route
import json

def planner(request):
    if request.method == 'POST':
        route_id = request.POST.get('route_id')
        route = get_object_or_404(Route, id=route_id)
        return render(request, 'planner.html', {'route': route})
    return render(request, 'planner.html')

@login_required
def save_route(request):
    if request.method == 'POST':
        user = request.user
        start = request.POST.get('start')
        end = request.POST.get('end')
        #waypoints = request.POST.get('waypoints')
        generated_waypoints = request.POST.get('generated_waypoints')
        distance = request.POST.get('distance')
        travel_time = request.POST.get('travel_time')

        route = Route.objects.create(
            user=user,
            start=start,
            end=end,
            waypoints=generated_waypoints,  # Salva i waypoints generati
            distance=distance,
            travel_time=travel_time
        )
        return JsonResponse({'status': 'success', 'route_id': route.id})

    return JsonResponse({'status': 'error'}, status=400)

def tour_view(request):
    routes=Route.objects.all()
    return render(request, 'tour.html', {'routes': routes})

def filter_view(request):
    start_search_query = request.GET.get('start_search', '')
    end_search_query = request.GET.get('ens_search', '')
    min_km = request.GET.get('min_km')
    max_km = request.GET.get('max_km')
    min_time = request.GET.get('min_time')
    max_time = request.GET.get('max_time')

    if min_km == '':
        min_km=0
    if max_km == '':
        max_km=100000
    if min_time == '':
        min_time=0
    if max_time == '':
        max_time=1000

    if not (str(min_km).isdigit() and str(max_km).isdigit() and str(min_time).isdigit() and str(max_time).isdigit()):
        routes=Route.objects.all()
        return render(request, 'tour.html', {'routes': routes})

    routes = Route.objects.filter(
        start__icontains=start_search_query, 
        end__icontains=end_search_query, 
        distance__gte=min_km, 
        distance__lte=max_km, 
        travel_time__gte=min_time, 
        travel_time__lte=max_time
    )

    return render(
        request, 
        'tour.html', {
            'routes': routes, 
        }
    )
