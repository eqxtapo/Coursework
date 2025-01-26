import json
from datetime import datetime

import pytest


@pytest.fixture
def month() -> datetime:
    return datetime(2025, 1, 1, 0, 0)


@pytest.fixture
def invest() -> str:
    result_list_dicts = {"month": "2021-12", "rounding_step": 10, "total_amount": 1187.69}

    json_output = json.dumps(result_list_dicts, ensure_ascii=False, indent=4)
    return json_output


@pytest.fixture
def page() -> str:
    result_list_dicts = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "*4556",
             "total_spent": 70951.8,
             "cashback": 709.52},
            {"last_digits": "*5441",
             "total_spent": 157204.0,
             "cashback": 1572.04},
            {"last_digits": "*7197",
             "total_spent": 51205.36,
             "cashback": 512.05}],
        "top_transactions": [
            {"date": "24.01.2018",
             "amount": 115909.42,
             "category": "Переводы",
             "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
            {"date": "10.01.2018",
             "amount": 30000.0,
             "category": "Пополнения",
             "description": "Перевод с карты"},
            {"date": "10.01.2018",
             "amount": 30000.0,
             "category": "Пополнения",
             "description": "Перевод с карты"},
            {"date": "10.01.2018",
             "amount": 27068.0,
             "category": "Пополнения",
             "description": "Перевод с карты"},
            {"date": "10.01.2018",
             "amount": 25100.0,
             "category": "Пополнения",
             "description": "Перевод с карты"}],
        "currency_rates": [
            {"currency": "USD",
             "rate": 97.805911},
            {"currency": "EUR",
             "rate": 102.731861}],
        "stock_prices": [
            {"stock": "AAPL",
             "price": 217.82605},
            {"stock": "AMZN",
             "price": 192.8868},
            {"stock": "GOOGL",
             "price": 172.52216},
            {"stock": "MSFT",
             "price": 425.42285},
            {"stock": "TSLA",
             "price": 255.27725}]}
    json_output = json.dumps(result_list_dicts, ensure_ascii=False, indent=4)
    return json_output
