"""The custom logic for the command m3 describe-service-section."""
import json

from bs4 import BeautifulSoup


def create_custom_response(request, response):
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response

    if isinstance(response, list):
        for res in response:
            block_value = res.get('blockValue')
            html = bool(BeautifulSoup(block_value, "html.parser").find())
            if html:
                res['blockValue'] = '<HTML content>'
    return response
