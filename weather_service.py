import os

import aiohttp.client
from aiogram.types import Location
from dotenv import load_dotenv
import json

load_dotenv()
WEATHER_SERVICE_API_KEY = os.getenv('WEATHER_SERVICE_API_KEY')
GEOCODE_API_KEY=os.getenv('GEOCODE_API_KEY')


status_dict = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "heavy-rain": "сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом"
}


class WeatherServiceException(BaseException):
    pass


class WeatherInfo:

    def __init__(self, temperature, status, is_kelvin=False):
        self.temperature = kelvin_to_celsius(
            temperature) if is_kelvin else temperature
        self.status = status_dict[status]

def get_city():
    global current_city
    return current_city

async def get_weather_for_city(city_name: str) -> WeatherInfo:
    return await make_weather_service_query(await get_city_query_url(city_name))


async def get_weather_for_location(location: Location) -> WeatherInfo:
    return await make_weather_service_query(get_location_query_url(location))


async def get_city_query_url(city_name: str):
    global current_city
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODE_API_KEY}&geocode={city_name}&kind=locality&format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            data = json.loads(text)
            if data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != '0':
                coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                if data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']["GeocoderMetaData"]['kind'] in ("locality", "province"):
                    latitude, longitude = map(float, coordinates.split())
                    current_city = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
                    return f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&extra=true'
    raise WeatherServiceException()

def get_location_query_url(location: Location):
    return f'http://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={WEATHER_SERVICE_API_KEY}&lang=ru'


async def make_weather_service_query(url: str) -> WeatherInfo:
    headers = headers = {
        'X-Yandex-API-Key': WEATHER_SERVICE_API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            text = await response.text()
            data = json.loads(text)
            if response.status == 200:
                return get_weather_from_response(data)

    raise WeatherServiceException()


def get_weather_from_response(json):
    return WeatherInfo(json['fact']['temp'], json['fact']['condition'])


def kelvin_to_celsius(degrees):
    KELVIN_0 = 273.15
    return degrees - KELVIN_0