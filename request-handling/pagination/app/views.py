import csv

from django.shortcuts import render_to_response, redirect
from django.urls import reverse

from django.core.paginator import Paginator
from urllib.parse import urlparse, urlencode

from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(BUS_STATION_CSV, encoding='cp1251') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        bus_stations = []
        for line in reader:
            bus_station_dict = {
                'Name': line['Name'],
                'Street': line['Street'],
                'District': line['District']
            }
            bus_stations.append(bus_station_dict)
    count = 10
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stations, count)
    page = paginator.get_page(page_num)
    data = page.object_list
    prev_page = urlencode({'page': page_num - 1})
    if page_num - 1 < 1:
        prev_page_url = None
    elif page_num - 1 == 1:
        prev_page_url = reverse('bus_stations')
    else:
        prev_page_url = reverse('bus_stations') + f'?{prev_page}'
    if len(bus_stations) % count != 0:
        count_pages = len(bus_stations) // count + 1
    else:
        count_pages = len(bus_stations) // count
    next_page = urlencode({'page': page_num + 1})
    if page_num + 1 > count_pages:
        next_page_url = None
    else:
        next_page_url = reverse('bus_stations') + f'?{next_page}'
    return render_to_response('index.html', context={
        'bus_stations': data,
        'current_page': page_num,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
