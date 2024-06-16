from api_to_dataframe.common.utils.retry_strategies import RetryStrategies


class Retainer:
    @staticmethod
    def strategy(retry_strategy: RetryStrategies = RetryStrategies.NoRetryStrategy):
        if retry_strategy == RetryStrategies.NoRetryStrategy:
            print("::: NoRetryStrategy :::")
        elif retry_strategy == RetryStrategies.LinearStrategy:
            print("::: LinearStrategy :::")
        elif retry_strategy == RetryStrategies.ExponentialStrategy:
            print("::: ExponentialStrategy :::")
        elif retry_strategy == RetryStrategies.CustomStrategy:
            print("::: CustomStrategy :::")

