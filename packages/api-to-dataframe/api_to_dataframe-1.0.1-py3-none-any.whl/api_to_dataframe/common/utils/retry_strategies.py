from enum import Enum


class RetryStrategies(Enum):
    NoRetryStrategy = 0
    LinearStrategy = 1
    ExponentialStrategy = 2
    CustomStrategy = 3

