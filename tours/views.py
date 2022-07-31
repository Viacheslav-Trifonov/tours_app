import random

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from .data import title, subtitle, description, departures, tours


def custom_handler404(request: WSGIRequest, exception) -> HttpResponse:
    return render(request, '404.html', status=400)


def custom_handler500(request: WSGIRequest) -> HttpResponse:
    return render(request, '500.html', status=500)


tours_with_num = []
for key, value in tours.items():
    value.setdefault('num', key)
    tours_with_num.append(value)


def main_view(request: WSGIRequest) -> HttpResponse:
    amount_random = []
    while len(amount_random) < 6:
        rand = random.randint(1, len(tours))
        if rand not in amount_random:
            amount_random.append(rand)

    random_6_hotels = []
    for tour in tours_with_num:
        if tour['num'] in amount_random:
            random_6_hotels.append(tour)

    context = {
        'departures': departures,
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'random_6_hotels': random_6_hotels
    }
    return render(request, 'tours/index.html', context=context)


def departure_view(request: WSGIRequest, departure: str) -> HttpResponse:
    flying_from = (departures[departure][:1].lower() + departures[departure][1:])
    hotels_departure = []
    for tour in tours_with_num:
        if tour['departure'] == departure:
            hotels_departure.append(tour)

    numbers_of_hotels = len(hotels_departure)
    max_price_of_hotels = max([hotels['price'] for hotels in hotels_departure])
    min_price_of_hotels = min([hotels['price'] for hotels in hotels_departure])
    max_nights = max([hotels['nights'] for hotels in hotels_departure])
    min_nights = min([hotels['nights'] for hotels in hotels_departure])

    context = {
        'departures': departures,
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'departure': departure,
        'flying_from': flying_from,
        'hotels_departure': hotels_departure,
        'numbers_of_hotels': numbers_of_hotels,
        'max_price_of_hotels': max_price_of_hotels,
        'min_price_of_hotels': min_price_of_hotels,
        'max_nights': max_nights,
        'min_nights': min_nights
    }
    return render(request, 'tours/departure.html', context=context)


def tour_view(request: WSGIRequest, num: int) -> HttpResponse:

    hotels_num = []
    for tour in tours_with_num:
        if tour['num'] == num:
            hotels_num.append(tour)

    departures_city = []
    for tour in tours_with_num:
        if tour['num'] == num:
            departures_city.append(tour['departure'])
    city = (departures[departures_city[0]]).split()
    context = {
        'departures': departures,
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'hotels_num': hotels_num,
        'name_city': city[1]
    }
    return render(request, 'tours/tour.html', context=context)
