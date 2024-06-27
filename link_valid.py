import scraper
import requests
from tqdm import tqdm

def link_valid(dataframe, status_code):
    for url in tqdm(dataframe['URL'], desc="Processing URLs", unit="url"):
        if url.startswith('s3://'):
            print(f"Skipping S3 URL: {url}")
            status_code.append(None)  # Append None for S3 URLs
            continue
        
        try:
            response = requests.head(url, timeout=5)  # Set a timeout of 5 seconds
            status_code.append(response.status_code)
        except requests.exceptions.InvalidSchema:
            print(f"Invalid schema found for URL: {url}")
            status_code.append(None)  # Append None to indicate the error
        except requests.exceptions.RequestException as e:
            # Catch other possible request exceptions, including timeouts
            print(f"Error fetching {url}: {e}")
            status_code.append(None)  # Append None to indicate the error

    dataframe['status_code'] = status_code
    dataframe.to_csv('aluswe.csv', index=False)

if __name__ == '__main__':
    dataframe = scraper.scraper()
    status_code = []
    link_valid(dataframe, status_code)