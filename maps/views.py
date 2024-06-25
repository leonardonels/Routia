from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Route

def planner(request):
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
