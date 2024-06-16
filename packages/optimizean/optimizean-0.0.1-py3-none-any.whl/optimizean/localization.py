import time
import requests
import warnings

warnings.filterwarnings(action="ignore")


def greetings():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    current_hour = int(current_time.split(" ")[-1].split(":")[0])

    if 6 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    elif 18 <= current_hour < 22:
        return "evening"
    elif 22 <= current_hour or current_hour < 6:
        return "night"
    else:
        raise ValueError("Wrong Time")


def get_location():
    response = requests.get("http://ip-api.com/json/")
    data = response.json()
    return data.get("country"), data.get("countryCode")


def get_local_greeting(greeting, country_code):
    greetings_dict = {
        "morning": {
            "US": "Good morning",
            "FR": "Bonjour",
            "ES": "Buenos días",
            "DE": "Guten Morgen",
            "IT": "Buongiorno",
            "PT": "Bom dia",
            "RU": "Доброе утро",
            "KR": "좋은 아침",
            "ZH": "早上好",
            "JA": "おはようございます",
            "HI": "सुप्रभात",
            "AR": "صباح الخير",
        },
        "afternoon": {
            "US": "Good afternoon",
            "FR": "Bon après-midi",
            "ES": "Buenas tardes",
            "DE": "Guten Tag",
            "IT": "Buon pomeriggio",
            "PT": "Boa tarde",
            "RU": "Добрый день",
            "KR": "좋은 점심",
            "ZH": "下午好",
            "JA": "こんにちは",
            "HI": "नमस्ते",
            "AR": "مساء الخير",
        },
        "evening": {
            "US": "Good evening",
            "FR": "Bonsoir",
            "ES": "Buenas noches",
            "DE": "Guten Abend",
            "IT": "Buona sera",
            "PT": "Boa noite",
            "RU": "Добрый вечер",
            "KR": "좋은 저녁",
            "ZH": "晚上好",
            "JA": "こんばんは",
            "HI": "शुभ संध्या",
            "AR": "مساء الخير",
        },
        "night": {
            "KR": "좋은 밤",
            "US": "Good night",
            "FR": "Bonne nuit",
            "ES": "Buenas noches",
            "DE": "Gute Nacht",
            "IT": "Buona notte",
            "PT": "Boa noite",
            "RU": "Спокойной ночи",
            "ZH": "晚安",
            "JA": "おやすみなさい",
            "HI": "शुभ रात्रि",
            "AR": "تصبح على خير",
        },
    }

    local_greeting = greetings_dict.get(greeting, {}).get(country_code, "Hello")

    return local_greeting


if __name__ == "__main__":
    greeting = greetings()
    country, country_code = get_location()
    local_greeting = get_local_greeting(greeting, country_code)

    print(local_greeting)
