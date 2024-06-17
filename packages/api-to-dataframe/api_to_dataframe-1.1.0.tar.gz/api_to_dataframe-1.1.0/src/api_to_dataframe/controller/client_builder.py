from api_to_dataframe.common.utils.retry_strategies import RetryStrategies
from api_to_dataframe.models.get_data import GetData


class ClientBuilder:
    def __init__(self,
                 endpoint: str,
                 headers: dict = {},
                 retry_strategy: RetryStrategies = RetryStrategies.NoRetryStrategy,
                 timeout: int = 5):
        """
        Initializes an instance of ClientBuilder.

        Args:
            endpoint (str): The API endpoint to be accessed.
            retry_strategy (RetryStrategies, optional): The retry strategy for the request. Default is NoRetryStrategy.
            timeout (int, optional): The timeout for the request. Default is 5 seconds.

        Raises:
            ValueError: If the endpoint is empty.
        """
        if endpoint == "":
            raise ValueError("::: endpoint param is mandatory :::")
        else:
            self.endpoint = endpoint
            self.retry_strategy = retry_strategy
            self.timeout = timeout
            self.headers = headers

    def get_api_data(self):
        """
        Retrieves data from the API using the defined endpoint and retry strategy.

        Returns:
            dict: The response from the API.
        """
        response = GetData.get_response(self.endpoint, self.headers, self.retry_strategy, self.timeout)
        return response

    @staticmethod
    def api_to_dataframe(response: dict):
        """
        Converts the API response into a DataFrame.

        Args:
            response (dict): The response from the API.

        Returns:
            DataFrame: The data converted into a DataFrame.
        """
        df = GetData.to_dataframe(response)
        return df
