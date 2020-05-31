from django.shortcuts import render, redirect
import requests
from. models import City
from.forms import CityForm


def index(request):
    appid = '99ff0df8160843f29dc132f959ac3fc3'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid + '&lang=ru'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()

                if res['cod'] == 200:
                    form.save()
                else:
                    err_msg = "Такого города не существет"
            else:
                err_msg = 'Такой город уже отображен'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in reversed(cities):

        res = requests.get(url.format(city.name)).json()

        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {
        'message' : message,
        'message_class' : message_class,
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather_app/wrapper.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
