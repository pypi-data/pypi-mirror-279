import requests
import pandas as pd

from api_to_dataframe.common.utils.retry_strategies import RetryStrategies


class GetData:
    @staticmethod
    def get_response(endpoint: str, RetryStrategies: RetryStrategies):
        response = requests.get(endpoint)

        if response.ok:
            return response.json()
        else:
            raise ConnectionError(response.status_code)

    @staticmethod
    def to_dataframe(response):
        df = pd.DataFrame(response)
        if df.empty:
            raise ValueError("::: DataFrame is empty :::")
        else:
            return df

