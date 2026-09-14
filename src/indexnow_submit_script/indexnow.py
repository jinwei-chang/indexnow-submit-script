import httpx

"""
    Search engines endpoints
    You can see here for more information: https://www.indexnow.org/faq
"""
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
BING_ENDPOINT = "https://www.bing.com/indexnow"


def submit_urls(host: str, key: str, urls: list[str], endpoint: str = "indexnow") -> httpx.Response:
    payload = {
        "host": host,
        "key": key,
        "urlList": urls,
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    search_engine_endpoint = BING_ENDPOINT if endpoint == "bing" else INDEXNOW_ENDPOINT

    response = httpx.post(search_engine_endpoint, json=payload, headers=headers)

    print(response.status_code)
    print("request endpoint:", response.request.url)

    return response
