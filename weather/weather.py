import requests


class Weather:
    def __init__(self):
        self.API_KEY = "396691b85924efcb35e47ccc3b827171"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def get_weather(self, city_name):
        complete_url = self.base_url + "appid=" + self.API_KEY + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            return x
        else:
            return None
