def run(event, context=None):
    import requests
    return requests.get('https://www.google.com/404').text