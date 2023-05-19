
import requests
import datetime
weather_dict = {
    "clear" : "ясно",
    "partly-cloudy" : "малооблачно",
    "cloudy" : "облачно с прояснениями",
    "overcast" : "пасмурно",
    "drizzle" : "морось",
    "light-rain" : "небольшой дождь",
    "rain" : "дождь",
    "moderate-rain" : "умеренно сильный дождь",
    "heavy-rain" : "сильный дождь",
    "continuous-heavy-rain" : "длительный сильный дождь",
    "showers" : "ливень",
    "wet-snow" : "дождь со снегом",
    "light-snow" : "небольшой снег",
    "snow" : "снег",
    "snow-showers" : "снегопад",
    "hail" : "град",
    "thunderstorm" : "гроза",
    "thunderstorm-with-rain" : "дождь с грозой",
    "thunderstorm-with-hail" : "гроза с градом"
    
    }



def get_current_hour():
    daytime = int(datetime.datetime.now().hour)
    if 0 <= daytime & daytime < 6:
        return "ночь1"
    if 6 <= daytime & daytime < 12:
        return "утро"
    if 12 <= daytime & daytime < 18:
        return "день"
    if 18 <= daytime & daytime < 23:
        return "вечер"
    if 23 <= daytime:
        return "ночь"
    

def yandex_weather_get():

    hello_phrase = ""

    time_current_string = get_current_hour()

    
    if time_current_string == "ночь":
            hello_phrase = "доброй ночи"
    if time_current_string == "ночь1":
            hello_phrase = "доброй ночи"
    if time_current_string =="утро":
            hello_phrase = "доброе утро"
    if time_current_string == "день":
            hello_phrase = "добрый день"
    if time_current_string == "вечер":
            hello_phrase = "добрый вечер"

    try:

        response = requests.request("GET",
                                   "https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&extra=false", 
                                   headers={'X-Yandex-API-Key': '60a29894-5bb4-4e5b-be3c-179423bc6334'},
                                   data={})
        final = response.json()
        print(final)
        weather_temp_current = str(final["fact"]["feels_like"])
        weather_cond_current = weather_dict[final["fact"]["condition"]]
        weather_day_temp = str(final["forecasts"][0]["parts"]["day"]["temp_avg"])
        weather_day_cond = weather_dict[str(final["forecasts"][0]["parts"]["day"]["condition"])]
        weather_evening_temp = str(final["forecasts"][0]["parts"]["evening"]["temp_avg"])
        weather_evening_cond = weather_dict[str(final["forecasts"][0]["parts"]["evening"]["condition"])]
        weather_morning_temp = str(final["forecasts"][0]["parts"]["morning"]["temp_avg"])
        weather_morning_cond = weather_dict[str(final["forecasts"][0]["parts"]["morning"]["condition"])]
    except Exception as e:
            print("Exception (weather):", e)
            pass            
        
    if time_current_string == "ночь":
        final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current 
    if time_current_string == "ночь1":
        final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current+ ". утром будет " + weather_evening_cond + ". на термометре будет " + weather_morning_temp + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp + ". а вечером " + weather_evening_cond + ". температура " + weather_evening_temp
    if time_current_string == "утро":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp + ". а вечером " + weather_evening_cond + ". температура " + weather_evening_temp   
    if time_current_string == "день":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". вечером будет " + weather_evening_cond + ". градусник покажет " + weather_evening_temp       
    if time_current_string == "вечер":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current
    print(final_string)

    