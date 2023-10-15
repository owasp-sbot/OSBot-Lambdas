#todo: add requests example to get google (or another site)
import requests

def run(event, context=None):
    return requests.get('https://www.google.com/404').text