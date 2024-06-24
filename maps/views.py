from django.shortcuts import render

def planner(request):
    return render(request, 'planner.html')
