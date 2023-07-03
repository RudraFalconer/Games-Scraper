# GamingSteamScrapper

## Pre-requisites

Install Python3, then execute in your terminal the following command:

```shell
python -m pip install -r source/requirements.txt
```

## Running the scrapper

```shell
python source/main.py
```

The output CSV containing the dataset can be found in the `dataset/` folder. A new CSV file will be generated for each run, and its name will contain the date and time of such run.

## Overcoming issues

1. **Certain game detail pages were unreachable due to a redirect loop**
   1. Infinite redirect loops found while using `requests` library, caused by several reasons (e.g. URLs containing special characters)
   2. Replacing `requests` library with `urllib` fixes the issue - it seems like both libraries handle redirection URL encoding in a different way, as explained [**here**](https://stackoverflow.com/a/51127373).