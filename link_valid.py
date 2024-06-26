import scraper
import requests


def link_valid(dataframe, status_code):
    for url in dataframe['URL']:
        response = requests.get(url)

        status_code.append(response.status_code)

    dataframe['status_code'] = status_code


if __name__ == '__main__':
    dataframe = scraper.scraper()
    status_code = []
    link_valid(dataframe, status_code)