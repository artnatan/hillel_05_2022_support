from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

import requests
from django.http import JsonResponse

# NOTE: directory name and file name
FILENAME_HISTORY = "history.json"
_PATH = "exchange_rates/logs"


def home(request):
    data = {"message": "hello from json response", "num": 12.2}
    return JsonResponse(data)


@dataclass
class ExchangeRate:
    from_: str
    to: str
    value: float

    @classmethod
    def from_response(cls, response: requests.Response) -> ExchangeRate:
        pure_response: dict = response.json()["Realtime Currency Exchange Rate"]
        from_ = pure_response["1. From_Currency Code"]
        to = pure_response["3. To_Currency Code"]
        value = pure_response["5. Exchange Rate"]

        return cls(from_=from_, to=to, value=value)

    def __eq__(self, other: ExchangeRate) -> bool:
        return self.value == other.value


ExchangeRates = list[ExchangeRate]


class ExchangeRatesHistory:

    _history: ExchangeRates = []

    # NOTE: combo directory + file
    history_log_path: str = os.path.join(_PATH, FILENAME_HISTORY)

    # NOTE: read json file
    @classmethod
    def read_history_file(cls) -> None:

        # NOTE: check if directory and file exist. If not, create
        if os.path.exists(cls.history_log_path):
            with open(cls.history_log_path, "r") as file:
                data = json.load(file)
                cls._history = data["results"]
        else:
            open(cls.history_log_path, "w")

    # NOTE: write json file
    @classmethod
    def write_history_file(cls, history_dict: dict) -> None:
        with open(cls.history_log_path, "w") as file:
            json.dump(history_dict, file)

    @classmethod
    def add(cls, instance: ExchangeRate) -> None:
        cls.read_history_file()
        # NOTE: instance is ExchangeRate and cls._history taken from file is dict. Bringing data to dict
        instance = asdict(instance)
        if not cls._history:
            cls._history.append(instance)
        elif cls._history[-1] != instance:
            cls._history.append(instance)

    @classmethod
    def as_dict(cls) -> dict:

        return {"results": [er for er in cls._history]}

    @classmethod
    def save_history(cls) -> dict:

        # NOTE: check if there is data in variable
        # if not, read the file and bring it to the final form
        if not cls._history:
            cls.read_history_file()
            history_dict = cls.as_dict()
        # if there is, bring to the final form
        elif cls._history:
            history_dict = cls.as_dict()

        cls.write_history_file(history_dict)
        return history_dict


def btc_usd(request):

    API_KEY = "GIS1LBGRBQ9NR24U"
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency"
        f"=BTC&to_currency=USD&apikey={API_KEY}"
    )

    response = requests.get(url)

    exchange_rate = ExchangeRate.from_response(response)
    ExchangeRatesHistory.add(exchange_rate)

    return JsonResponse(asdict(exchange_rate))


def history(request):
    return JsonResponse(ExchangeRatesHistory.save_history())
