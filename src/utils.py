import json
import logging
import os
from datetime import datetime as dt
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY_RATES = os.getenv("API_KEY_RATES")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")

# Получаем абсолютный путь до текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем путь до файла логов относительно текущей директории
rel_log_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_log_file_path = os.path.abspath(rel_log_file_path)

# Создаем путь до файла user_settings.json относительно текущей директории.
rel_json_path = os.path.join(current_dir, "../data/user_settings.json")
abs_json_path = os.path.abspath(rel_json_path)

# Создаем путь до файла operations.xlsx относительно текущей директории
rel_xlsx_path = os.path.join(current_dir, "../data/operations.xlsx")
abs_xlsx_path = os.path.abspath(rel_xlsx_path)

# Добавляем логгер, который записывает логи в файл.
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Создаем json-файл со списком акций и валют

currencies_stocks_dict = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}

with open(abs_json_path, "w") as file:
    json.dump(currencies_stocks_dict, file)


def import_from_excel(input_xlsx_file: str) -> pd.DataFrame:
    """Функция принимает на вход путь до файла xlsx и возвращает DataFrame"""

    input_df = pd.read_excel(input_xlsx_file)

    try:
        logger.info("Данные из файла xlsx импортированы")

        return input_df
    except Exception:
        logger.warning("Импортируемый список пуст или отсутствует.")
        return input_df


df = import_from_excel(abs_xlsx_path)


def get_currency_rates(json_file: str) -> list[Any]:
    """Функция принимает на вход json-файл и возвращает список словарей с курсами требуемых валют.
    Курс валюты функция импортирует через API"""
    logger.info("Курсы валют получены")
    with open(json_file, "r", encoding="utf-8") as file:

        currencies_stocks_list = json.load(file)
        currency_rates_list_dicts = []

        for i in currencies_stocks_list["user_currencies"]:

            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={i}"

            headers = {"apikey": API_KEY_RATES}

            response = requests.get(url, headers=headers)
            result = response.json()

            currency_rates_dict = {"currency": i, "rate": result["rates"].get("RUB")}
            currency_rates_list_dicts.append(currency_rates_dict)

        return currency_rates_list_dicts


def get_stock_prices(json_file: str) -> list[Any]:
    """Функция принимает на вход json-файл и возвращает список словарей с курсами требуемых акций.
    Стоимости акций функция импортирует через API"""
    logger.info("Стоимости акций получены")
    with open(json_file, "r", encoding="utf-8") as file:

        currencies_stocks_list = json.load(file)
        stock_prices_list_dicts = []

        for i in currencies_stocks_list["user_stocks"]:

            url = f"https://financialmodelingprep.com/api/v3/quote/{i}?apikey={API_KEY_STOCKS}"

            response = requests.get(url)

            result = response.json()

            stock_prices_dicts = {"stock": i, "price": result[0].get("priceAvg200")}
            stock_prices_list_dicts.append(stock_prices_dicts)

        return stock_prices_list_dicts


input_datetime = "2018-02-16 12:01:58"


def greetings(input_datetime: str) -> str:
    """Функция принимает строку с датой и возвращает требуемое приветствие"""
    date_update = dt.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
    time = date_update.strftime("%H:%M:%S")

    if time > "05:00:00" and time <= "12:00:00":
        return "Доброе утро"
    if time > "12:00:00" and time <= "18:00:00":
        return "Добрый день"
    if time > "18:00:00" and time <= "23:00:00":
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def start_month(input_datetime: str) -> dt:
    """Функция принимает на вход строку с датой и возвращает начало месяца"""
    date_update = dt.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")
    start = date_update.replace(day=1, hour=0, minute=0, second=0)
    return start


begin_month = start_month(input_datetime)


def filter_date(df_test: str) -> pd.DataFrame:
    """Функция создает DataFrame по заданному периоду времени"""
    df = pd.read_excel(df_test)
    df_date = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_df_to_date = df[(begin_month <= df_date) & (df_date <= input_datetime)]
    return filtered_df_to_date


filtered_to_date = filter_date(abs_xlsx_path)


def cards_info(input_df: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция принимает на вход путь до файла xlsx и возвращает DataFrame"""

    df_input = input_df
    df_output = []
    try:
        logger.info("Данные из файла xlsx импортированы")

        cards = df_input.groupby("Номер карты")
        cards_prices = cards["Сумма операции с округлением"].sum()
        df_test = cards_prices.to_dict()

        for cards, sum in df_test.items():
            df_result = {}
            df_result["last_digits"] = cards
            df_result["total_spent"] = sum
            df_result["cashback"] = round(sum / 100, 2)
            df_output.append(df_result)
        return df_output
    except Exception:
        logger.warning("Импортируемый список пуст или отсутствует.")
        return [{}]


def top_transactions(input_df: pd.DataFrame) -> list[dict[str, Any]] | None:
    """Функция принимает на вход DataFrame и возвращает ТОП-5 транзакций по сумме платежа"""
    df_input_sort = input_df
    df_output_sort = []
    try:
        logger.info("Данные из файла xlsx импортированы")

        sorted_df = df_input_sort.sort_values("Сумма платежа", ascending=False)
        sort_five = sorted_df.iloc[0:5]

        df_sort_dict = sort_five.to_dict("records")
        for i in df_sort_dict:
            df_sort_result = {}
            df_sort_result["date"] = i["Дата платежа"]
            df_sort_result["amount"] = i["Сумма платежа"]
            df_sort_result["category"] = i["Категория"]
            df_sort_result["description"] = i["Описание"]
            df_output_sort.append(df_sort_result)
        return df_output_sort
    except Exception:
        logger.warning("Импортируемый список пуст или отсутствует.")
        return None


def format_date(input_datetime: str) -> str:
    """Функция форматирует дату"""
    date_update = dt.strptime(input_datetime, "%d.%m.%Y")
    return date_update.strftime("%Y-%m-%d")
