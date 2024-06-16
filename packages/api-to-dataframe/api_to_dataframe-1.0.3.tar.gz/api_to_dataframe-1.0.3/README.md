# API to DataFrame
Your solution to convert API responses to Pandas DataFrames with retry strategies and detailed reports.

[![Github](https://img.shields.io/badge/-Go_to_Github_repository-05122A?style=flat&logo=github)](https://github.com/IvanildoBarauna/api-to-dataframe)

[![PyPI - Status](https://img.shields.io/pypi/status/api-to-dataframe?style=for-the-badge&logo=pypi)](https://pypi.org/project/api-to-dataframe/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/api-to-dataframe?style=for-the-badge&logo=pypi)](https://pypi.org/project/api-to-dataframe/)
[![PyPI - Version](https://img.shields.io/pypi/v/api-to-dataframe?style=for-the-badge&logo=pypi)](https://pypi.org/project/api-to-dataframe/#history)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/api-to-dataframe?style=for-the-badge&logo=python)

[![CI](https://img.shields.io/github/actions/workflow/status/IvanildoBarauna/api-to-dataframe/CI.yaml?&style=for-the-badge&logo=githubactions&cacheSeconds=60&label=Tests+and+pre+build)](https://github.com/IvanildoBarauna/api-to-dataframe/actions/workflows/CI.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/IvanildoBarauna/api-to-dataframe/CD.yaml?&style=for-the-badge&logo=githubactions&cacheSeconds=60&event=release&label=Package_publication)](https://github.com/IvanildoBarauna/api-to-dataframe/actions/workflows/CD.yaml)

[![Codecov](https://img.shields.io/codecov/c/github/IvanildoBarauna/api-to-dataframe?style=for-the-badge&logo=codecov)](https://app.codecov.io/gh/IvanildoBarauna/api-to-dataframe)

## Project Stack

![Python](https://img.shields.io/badge/-Python-05122A?style=flat&logo=python)&nbsp;
![Docker](https://img.shields.io/badge/-Docker-05122A?style=flat&logo=docker)&nbsp;
![Poetry](https://img.shields.io/badge/-Poetry-05122A?style=flat&logo=poetry)&nbsp;
![GitHub Actions](https://img.shields.io/badge/-GitHub_Actions-05122A?style=flat&logo=githubactions)&nbsp; 
![CodeCov](https://img.shields.io/badge/-CodeCov-05122A?style=flat&logo=codecov)&nbsp;
![pypi](https://img.shields.io/badge/-pypi-05122A?style=flat&logo=pypi)&nbsp;
![pandas](https://img.shields.io/badge/-pandas-05122A?style=flat&logo=pandas)&nbsp;
![pytest](https://img.shields.io/badge/-pytest-05122A?style=flat&logo=pytest)&nbsp;



## Library Description

Python library that simplifies obtaining data from API endpoints by converting them directly into Pandas DataFrames. This library offers robust features, including retry strategies for failed requests and automatic generation of detailed reports on the received data.

## Installation

To install the package using pip, use the following command:

```sh
pip install api-to-dataframe
```

To install the package using poetry, use the following command:

```sh
poetry add api-to-dataframe
```

## How to use it

``` python
## Importing library
from api_to_dataframe import ClientBuilder, RetryStrategies

# Create a client for the API without retry strategy
client = ClientBuilder(endpoint="https://api.example.com", retry_strategy=RetryStrategies.NoRetryStrategy)
# or with LinearStrategy (In development, actually don't nothing)
client = ClientBuilder(endpoint="https://api.example.com", retry_strategy=RetryStrategies.LinearStrategy)

# Get data from the API
data = client.get_api_data()

# Convert the data to a DataFrame
df = client.api_to_dataframe(data)

# Display the DataFrame
print(df)
```