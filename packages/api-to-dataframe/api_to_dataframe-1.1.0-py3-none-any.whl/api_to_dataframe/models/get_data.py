import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import pandas as pd

from api_to_dataframe.common.utils.retry_strategies import RetryStrategies


class GetData:
    @staticmethod
    def get_response(endpoint: str,
                     headers: dict,
                     retry_strategies: RetryStrategies,
                     timeout: int):
        try:
            response = requests.get(endpoint, timeout=timeout, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise http_err
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            raise timeout_err
        else:
            return response

    @staticmethod
    def to_dataframe(response):
        try:
            df = pd.DataFrame(response.json())
        except Exception as err:
            raise TypeError(f"Invalid response for transform in dataframe: {err}")

        if df.empty:
            raise ValueError("::: DataFrame is empty :::")
        else:
            return df
