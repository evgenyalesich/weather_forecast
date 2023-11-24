from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    appid = '6d2fafeec7fab5a7403e205887f2688e'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        form = CityForm()
    else:
       form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        try:
            res = requests.get(url.format(city.name, appid)).json()
            if res.get("weather"):
                weather_condition = res.get("weather")[0].get("main").lower()

                if weather_condition in ['clear', 'clouds']:
                    weather_condition = 'clear'
                elif weather_condition in ['mist', 'smoke', 'haze', 'fog', 'sand', 'dust', 'ash', 'squall', 'tornado']:
                    weather_condition = 'cloudy'
                elif weather_condition in ['drizzle', 'rain', 'thunderstorm']:
                    weather_condition = 'rainy'
                elif weather_condition in ['snow', 'sleet', 'shower sleet', 'rain and snow', 'shower snow']:
                    weather_condition = 'snowy'
                else:
                    weather_condition = 'clear'
            else:
                weather_condition = 'clear'

            city_info = {
                'city': city.name,
                'temp': res.get("main").get("temp"),
                'icon': res.get("weather")[0].get("icon"),
                'pressure': res.get("main").get("pressure"),
                'humidity': res.get("main").get("humidity"),
                'weather_condition': weather_condition  ## ADD WEATHER CONDITION TO THE CITY INFO
            }
            all_cities.append(city_info)
        except Exception as ex:
            print(str(ex))
            pass

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)
