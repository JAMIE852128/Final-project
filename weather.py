import requests 
from datetime import datetime, timedelta, date
#weather api
weather_api_key = 'f17f637e959d448ead083204252105'

#check the city is exist or validate
def validate_city(city):
    test_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
    response = requests.get(test_url)
    data = response.json()
    if 'error' in data:
        return False
    return True

##################suggestion start##################
#check the date
def get_weatherData(city, start_date, end_date):
    current_date = datetime.now()  #give the yyyy-mm-dd
    total_days = (end_date - start_date).days + 1
    #all the dates are out of 14days
    if start_date > current_date + timedelta(days = 14):
        print('the date is too far in the future, we can only get the weather data for 14 days')
        print('\n————Here is the weather data of the same period in the last year————')
        get_historyData(city, start_date, end_date)
    #part of the dates are out of 14days
    elif start_date <= current_date + timedelta(days = 14) and end_date > current_date + timedelta(days = 14):
        middle_date = current_date + timedelta(days = 14)
        print('Sorry,we can only get the weather data for 14 days in the future')
        print(f'\n————Here is the forecast from {start_date} to {middle_date}————')
        get_futureData(city, start_date, middle_date)
        print(f'\n————Here is the last year weather in 【{city}】 from {middle_date+timedelta(days = 1)} to {end_date}————')
        get_historyData(city, middle_date+timedelta(days = 1), end_date)
    #all the dates are in the 14days
    elif end_date <= current_date + timedelta(days = 14):
        print(f'\n————Here is the weather forecase in 【{city}】 from {start_date} to {end_date}————')
        get_futureData(city, start_date, end_date)
    return 
#future date forecast
def get_futureData(city, start_date, end_date):
    avg_temp = []
    min_temp = []
    max_temp = []
    temp_range = []
    condition = []
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        url = f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&dt={date}"
        response = requests.get(url)
        data = response.json()
        # check data is not empty
        if 'forecast' not in data or 'forecastday' not in data['forecast'] or not data['forecast']['forecastday']:
            print(f"No data for {date.strftime('%Y-%m-%d')}. Skipping.")
            continue
        day = data['forecast']['forecastday'][0]['day']
        avg_temp.append(day['avgtemp_c'])
        min_temp.append(day['mintemp_c'])
        max_temp.append(day['maxtemp_c'])
        temp_range.append(day['maxtemp_c'] - day['mintemp_c'])
        condition.append(day['condition']['text'])
    #give suggestion
    if avg_temp:
        if len(avg_temp) == 1:
            print(f'\n{start_date.strftime("%Y-%m-%d")}: Average Temperature:{avg_temp[0]}˚C, Minimum Temperature: {min_temp[0]}˚C, Maximum Temperature: {max_temp[0]}˚C, condition: {condition[0]}')
            #suggest_clothing(avg_temp[0], min_temp[0], max_temp[0], temp_range[0], condition[0])
            advisor = ClothingAdvisor()
            advisor.suggest(avg_temp[0], min_temp[0], max_temp[0], temp_range[0], condition[0])
            print()
        #give summary
        elif len(avg_temp)>1:
            d_avg_temp = sum(avg_temp)/len(avg_temp)
            d_min_temp = min(min_temp)
            d_max_temp = max(max_temp)
            f_condition = max(set(condition), key=condition.count)
            print(f'\n✨Summary from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}✨\nAverage Temperature: {d_avg_temp:.2f}˚C, Minimum Temperature: {d_min_temp}˚C, Maximum Temperature: {d_max_temp}˚C, most common condition: {f_condition}')
            #give everyday weather and suggestion
            print('\nDetails below:')
            advisor = ClothingAdvisor()
            for i in range((end_date - start_date).days + 1):
                date = start_date + timedelta(days=i)
                print(f'\n{date.strftime("%Y-%m-%d")}: Average Temperature:{avg_temp[i]}˚C, Minimum Temperature: {min_temp[i]}˚C, Maximum Temperature: {max_temp[i]}˚C, condition: {condition[i]}')
                #suggest_clothing(avg_temp[i], min_temp[i], max_temp[i], temp_range[i], condition[i])
                advisor.suggest(avg_temp[i], min_temp[i], max_temp[i], temp_range[i], condition[i])
            print('\n～～～～～～～～～～～～～～～～～～～～～～～～') 
            print("🧳 Suggested clothing to pack:")
            for item, count in advisor.summary().items():
                print(f"{item}: {count} piece(s)")    
            print('～～～～～～～～～～～～～～～～～～～～～～～～\n')    
    return 

def get_historyData(city, start_date, end_date):
    avg_temp_h = []
    min_temp_h = []
    max_temp_h = []
    temp_range_h = []
    condition_h = []
    for i in range((end_date - start_date).days + 1):
        date = start_date - timedelta(days=365 + i)
        url = f"http://api.weatherapi.com/v1/history.json?key={weather_api_key}&q={city}&dt={date.strftime('%Y-%m-%d')}"
        response = requests.get(url)
        data = response.json()
        # check data is not empty
        if 'forecast' not in data or 'forecastday' not in data['forecast'] or not data['forecast']['forecastday']:
            print(f"No data for {date.strftime('%Y-%m-%d')}. Skipping.")
            continue
        day = data['forecast']['forecastday'][0]['day']
        avg_temp_h.append(day['avgtemp_c'])
        min_temp_h.append(day['mintemp_c'])
        max_temp_h.append(day['maxtemp_c'])
        temp_range_h.append(day['maxtemp_c'] - day['mintemp_c'])
        condition_h.append(day['condition']['text'])
    if avg_temp_h:
        if len(avg_temp_h) == 1:
            print(f'\n{start_date.strftime("%Y-%m-%d")}: Average Temperature:{avg_temp_h[0]}˚C, Minimum Temperature: {min_temp_h[0]}˚C, Maximum Temperature: {max_temp_h[0]}˚C, condition: {condition_h[0]}')
            #suggest_clothing(avg_temp_h[0], min_temp_h[0], max_temp_h[0], temp_range_h[0], condition_h[0])
            advisor = ClothingAdvisor()
            advisor.suggest(avg_temp_h[0], min_temp_h[0], max_temp_h[0], temp_range_h[0], condition_h[0])
            print()
        elif len(avg_temp_h) > 1:
            d_avg_temp_h = sum(avg_temp_h)/len(avg_temp_h)
            d_min_temp_h = min(min_temp_h)
            d_max_temp_h = max(max_temp_h)
            f_condition_h = max(set(condition_h), key=condition_h.count)
            print(f'\n✨last year Summary from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}✨\nAverage Temperature: {d_avg_temp_h:.2f}˚C, Minimum Temperature: {d_min_temp_h}˚C, Maximum Temperature: {d_max_temp_h}˚C, most common condition: {f_condition_h}')
            print('\nDetails below:')
            advisor = ClothingAdvisor()
            for i in range((end_date - start_date).days + 1):
                date = start_date + timedelta(days=i) - timedelta(days = 365)
                print(f'\n{date.strftime("%Y-%m-%d")}: Average Temperature:{avg_temp_h[i]}˚C, Minimum Temperature: {min_temp_h[i]}˚C, Maximum Temperature: {max_temp_h[i]}˚C, condition: {condition_h[i]}')
                #suggest_clothing(avg_temp_h[i], min_temp_h[i], max_temp_h[i], temp_range_h[i], condition_h[i])
                advisor.suggest(avg_temp_h[i], min_temp_h[i], max_temp_h[i], temp_range_h[i], condition_h[i])
            print('\n～～～～～～～～～～～～～～～～～～～～～～～～')
            print("🧳 Suggested clothing to pack:")
            for item, count in advisor.summary().items():
                print(f"{item}: {count} piece(s)")
            print('～～～～～～～～～～～～～～～～～～～～～～～～\n')  
    return 
"""
def suggest_clothing(avg_temp, min_temp, max_temp, temp_range, condition):
    if avg_temp > 28 :
        print('☀️👕It is hot, wear shorts and a t-shirt, bring some sun protection')
    elif avg_temp > 20 and avg_temp <= 28:
        print('🌤️👖It is warm, long pants with long sleeves, or have a thin jacket.')
    elif avg_temp > 10 and avg_temp <=20:
        print('🍁🧥It is cold, wear a hoodie, thick jacket and pants.')
    elif avg_temp <= 10:
        print('❄️🧣It is frigid, put on your sweaters and down jackets')
    if 'rain' in condition.lower():
        print('🌂There might be rain, bring an umbrella')
    elif 'snow' in condition.lower():
        print('🥾There might be snow, wear waterproof boots and coat')
    elif 'sunny' in condition.lower():
        print('🕶️It is a sunny day, wear sunglasses and suncream.')
    if temp_range > 10:
        print('The temperature change range is large, wear layers to adjust.')
    return 
"""

class ClothingAdvisor:
    def __init__(self):
        self.clothing_items = {}

    def add_item(self, item):
        if item in self.clothing_items:
            self.clothing_items[item] += 1
        else:
            self.clothing_items[item] = 1

    def suggest(self, avg_temp, min_temp, max_temp, temp_range, condition):
        # basic suggest
        if avg_temp > 28:
            print('☀️👕It is hot, wear shorts and a t-shirt, bring some sun protection')
            self.add_item('t-shirt')
            self.add_item('shorts')
        elif avg_temp > 20:
            print('🌤️👖It is warm, long pants with long sleeves, or a thin jacket.')
            self.add_item('long pants')
            self.add_item('long sleeves')
        elif avg_temp > 10:
            print('🍁🧥It is cool, wear a hoodie, thick jacket and pants.')
            self.add_item('hoodie')
            self.add_item('jacket')
            self.add_item('pants')
        else:
            print('❄️🧣It is frigid, put on your sweaters and down jackets')
            self.add_item('sweater')
            self.add_item('down jacket')
        # condition suggest
        if 'rain' in condition.lower():
            print('🌂There might be rain, bring an umbrella')
            self.add_item('umbrella')
        elif 'snow' in condition.lower():
            print('🥾There might be snow, wear waterproof boots and coat')
            self.add_item('waterproof coat')
            self.add_item('boots')
        elif 'sunny' in condition.lower():
            print('🕶️It is a sunny day, wear sunglasses and sunscreen.')
            self.add_item('sunglasses')
            self.add_item('sunscreen')
        if temp_range > 10:
            print('The temperature change range is large, wear layers to adjust.')
            self.add_item('layered clothes')
        self.add_item('underwear')
        self.add_item('socks')

    def summary(self):
        return self.clothing_items
        

def main():
    while True:
        city = input('please eneter the city name:')
        if validate_city(city):
            break
        else:
            print('The city is not found, please check the spelling or try another city.')
    
    start_str = input('please enter the start date (yyyy-mm-dd):')
    end_str = input('please enter the end date (yyyy-mm-dd):')
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")

        if end_date < start_date:
            print('The end date must be after the start date.')
            return
        if start_date < datetime.now():
            print('The start date must be after today.')
            return
        #get the summary of clothes need to bring

        #get the weather and clothing suggestion for each day
        get_weatherData(city, start_date, end_date)
    except ValueError:
        print('Invalid date format, please use yyyy-mm-dd.')

if __name__ == '__main__':
    main()
