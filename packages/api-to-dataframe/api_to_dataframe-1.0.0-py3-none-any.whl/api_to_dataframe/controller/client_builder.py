from api_to_dataframe.common.utils.retry_strategies import RetryStrategies
from api_to_dataframe.models.get_data import GetData


class ClientBuilder:
    def __init__(self, endpoint: str, retry_strategy: RetryStrategies = RetryStrategies.NoRetryStrategy):
        if endpoint == "":
            raise ValueError("::: endpoint param is mandatory :::")
        else:
            self.endpoint = endpoint
            self.retry_strategy = retry_strategy

    def get_api_data(self):
        response = GetData.get_response(self.endpoint, self.retry_strategy)
        return response

    @staticmethod
    def api_to_dataframe(response: dict):
        df = GetData.to_dataframe(response)
        return df
