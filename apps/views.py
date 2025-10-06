from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime


try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo


def welcome(request):
    return render(request,'welcome.html')

def users(request):
    users = [
        {'full_name' : 'Argynbekuly Kydyrali', 'age': 20,},
        {'full_name' : 'Gainullin Dinur' , 'age' : 19,},

    ]

    return render(request,'users_list.html', {'users': users})

def city_time(request):
    cities = {
        'Almaty': 'Asia/Almaty',
        'Calgary': 'America/Edmonton',   
        'Moscow': 'Europe/Moscow',
        'UTC': 'UTC',
    }
    selected = request.GET.get('city', None)
    current_time = None
    if selected in cities:
        tz_name = cities[selected]
        try:
            tz = ZoneInfo(tz_name)
            current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        except Exception as e:
            current_time = f"Time zone error: {e}"
    return render(request, 'city_time.html', {
        'cities': list(cities.keys()),
        'selected': selected,
        'current_time': current_time,
    })

def counter_view(request):
    cnt = request.session.get('counter', 0)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'inc':
            cnt += 1
            request.session['counter'] = cnt
        elif action == 'reset':
            cnt = 0
            request.session['counter'] = cnt
        return HttpResponseRedirect(reverse('counter'))

    return render(request, 'counter.html', {'counter': cnt})