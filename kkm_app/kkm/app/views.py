import json
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .for_views.utils import *
from .for_views.constaints import *


BASE_DIR = settings.BASE_DIR


def kkm_index(request):
    # Получаем текущее время и дату
    now = datetime.now()
    
    # Форматируем время
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d.%m.%Y")
    
    # Передаем данные в шаблон
    context = {
        'current_time': current_time,
        'current_date': current_date,
    }
    
    # Если это AJAX запрос, возвращаем только данные
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse(context)
    
    return render(request, 'app/index.html', context)

def cart_of_patient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            birthday = data.get('birthday')
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
            
            result = {
                'success': True,
                'birthday_result': birthday_date,
                'cart_of_patient': get_cart(birthday_date)
            }
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        