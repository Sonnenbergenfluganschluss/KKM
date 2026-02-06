# import json
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse  # если нужен AJAX
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

birthday = '1983-12-09'

def cart_of_patient():
    year = int(birthday[:4])
    polugodie = read_files('Полугодия', 'year')
    if birthday in polugodie.loc[year, "I полугодие"]:
        # st.markdown(f"I полугодие {year} года")
        polugodie_true = "I полугодие"
        polugodie_false = "II полугодие"
    elif birthday in polugodie.loc[year, "II полугодие"]:
        # st.markdown(f"II полугодие {year} года")
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
    else:
        # st.markdown(f"II полугодие {year-1} года")
        polugodie_true = "II полугодие"
        polugodie_false = "I полугодие"
        year = year-1

    df = get_cart(year=year)
    
    if df.loc["Zang Fu Xu", "Используем"] == None:
        Zang_Fu_Xu = set()
    else:
        Zang_Fu_Xu = set(df.loc["Zang Fu Xu", "Используем"])

        