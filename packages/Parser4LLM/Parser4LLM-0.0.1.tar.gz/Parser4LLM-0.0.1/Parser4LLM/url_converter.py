import requests

class URLConverter:
    def __init__(self, base_url='https://r.jina.ai/'):
        self.base_url = base_url
        self.headers = {
            "Accept": "application/pdf",
            "X-Return-Format": "markdown",
        }

    def convert(self, url):
        md_url = f'{self.base_url}{url}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text, md_url
        else:
            return f'Request failed with status code: {response.status_code} for URL: {url}'