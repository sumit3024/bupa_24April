import requests
import json
import datetime


def get_exchange_rates(base_currency, target_currency, days):
    try:

        today_date = datetime.datetime.now()
        date_30day = (today_date - datetime.timedelta(days=days))

        # json to get data for last 30 days
        url = f'http://api.exchangeratesapi.io/v1/latest?access_key=205ecf4e7bb97999eb707a9e10263a55&from=base_currency&to=target_currency&start_date=today_date&end_date=date_30day'
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch exchange rates data.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)
    return None


# Preprocess the data
def preprocess_data(data):
    try:
        rates = data['rates']
        temp_dict = {'EUR': data['rates'][base_currency], 'NZD': data['rates'][target_currency]}
        return temp_dict

    except ValueError as e:
        print("Error occurred while Preprocessing data:", e)
        return None


# best and worst exchange rates for 30 days period
def find_best_and_worst_exchange_rates(rates):
    try:
        best_rate = max(rates.values())
        worst_rate = min(rates.values())
        return best_rate, worst_rate

    except ValueError as e:
        print("Error occurred while finding best and worst rates:", e)
        return None, None


# Average exchange rate for the month
def calculate_average_exchange_rate(rates):
    try:
        return sum(rates.values()) / len(rates)
    except ZeroDivisionError as e:
        print("Error occurred while calculating average rate:", e)
        return None


if __name__ == "__main__":
    base_currency = "EUR"
    target_currency = "NZD"
    days = 30

    exchange_rates_data = get_exchange_rates(base_currency, target_currency, days)
    if exchange_rates_data:
        rates = preprocess_data(exchange_rates_data)
        if rates:
            with open("exchange_rates_data.json", "w") as json_file:
                json.dump(rates, json_file, indent=4)
                print("json file generated")
        else:
            print("failed to generate json file")

    best_rate, worst_rate = find_best_and_worst_exchange_rates(rates)
    average_rate = calculate_average_exchange_rate(rates)

    print(f"Best exchange rate: 1 {base_currency} = {best_rate} {target_currency}")
    print(f"Worst exchange rate: 1 {base_currency} = {worst_rate} {target_currency}")
    print(f"Average exchange rate for the month: {average_rate} {target_currency}")

else:
    print("Failed to fetch exchange rates data.")
