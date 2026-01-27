# import json
# import pandas as pd
from datetime import datetime, timedelta, date
# import re
# import os
# from itertools import cycle
# import logging
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.http import JsonResponse  # если нужен AJAX


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
        