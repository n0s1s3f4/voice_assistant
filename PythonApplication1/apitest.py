
import requests
import datetime
weather_dict = {
    "clear" : "����",
    "partly-cloudy" : "�����������",
    "cloudy" : "������� � ������������",
    "overcast" : "��������",
    "drizzle" : "������",
    "light-rain" : "��������� �����",
    "rain" : "�����",
    "moderate-rain" : "�������� ������� �����",
    "heavy-rain" : "������� �����",
    "continuous-heavy-rain" : "���������� ������� �����",
    "showers" : "������",
    "wet-snow" : "����� �� ������",
    "light-snow" : "��������� ����",
    "snow" : "����",
    "snow-showers" : "��������",
    "hail" : "����",
    "thunderstorm" : "�����",
    "thunderstorm-with-rain" : "����� � ������",
    "thunderstorm-with-hail" : "����� � ������"
    
    }



def get_current_hour():
    daytime = int(datetime.datetime.now().hour)
    if 0 <= daytime & daytime < 6:
        return "����1"
    if 6 <= daytime & daytime < 12:
        return "����"
    if 12 <= daytime & daytime < 18:
        return "����"
    if 18 <= daytime & daytime < 23:
        return "�����"
    if 23 <= daytime:
        return "����"
    

def yandex_weather_get():

    hello_phrase = ""

    time_current_string = get_current_hour()

    
    if time_current_string == "����":
            hello_phrase = "������ ����"
    if time_current_string == "����1":
            hello_phrase = "������ ����"
    if time_current_string =="����":
            hello_phrase = "������ ����"
    if time_current_string == "����":
            hello_phrase = "������ ����"
    if time_current_string == "�����":
            hello_phrase = "������ �����"

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
        
    if time_current_string == "����":
        final_string = hello_phrase + ". ������ �� ����� " + weather_cond_current + ". ����������� ��������� ��� " + weather_temp_current 
    if time_current_string == "����1":
        final_string = hello_phrase + ". ������ �� ����� " + weather_cond_current + ". ����������� ��������� ��� " + weather_temp_current+ ". ����� ����� " + weather_evening_cond + ". �� ���������� ����� " + weather_morning_temp + ". ���� ������ ����� ����� " + weather_day_cond + ". ��������� ������� " + weather_day_temp + ". � ������� " + weather_evening_cond + ". ����������� " + weather_evening_temp
    if time_current_string == "����":
         final_string = hello_phrase + ". ������ �� ����� " + weather_cond_current + ". ����������� ��������� ��� " + weather_temp_current + ". ���� ������ ����� ����� " + weather_day_cond + ". ��������� ������� " + weather_day_temp + ". � ������� " + weather_evening_cond + ". ����������� " + weather_evening_temp   
    if time_current_string == "����":
         final_string = hello_phrase + ". ������ �� ����� " + weather_cond_current + ". ����������� ��������� ��� " + weather_temp_current + ". ������� ����� " + weather_evening_cond + ". ��������� ������� " + weather_evening_temp       
    if time_current_string == "�����":
         final_string = hello_phrase + ". ������ �� ����� " + weather_cond_current + ". ����������� ��������� ��� " + weather_temp_current
    print(final_string)

    