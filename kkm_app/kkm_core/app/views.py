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
# from django.http import JsonResponse  # если нужен AJAX

def kkm_index(request):
    context = {
        'title': 'KKM',
        'current_date_show': datetime.now().strftime("%d.%m.%Y"),
        'current_time_show': datetime.now().time()
    }
    return render(request, 'app/index.html', context)