import json

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def open_request(request: Request) -> any:
    """
    Generic method to open a Request object and return the JSON response
    :param request: Correctly initialized urllib.request.Request to be opened
    :return: JSON response (if any) from opening the request
    """
    try:
        # Open request and read the response
        response = urlopen(request)
        response_data = response.read().decode('utf-8')

        # If API responded with success
        if response.code == 200:
            # Return the jsonification of the response
            return json.loads(response_data)

        # Print errors returned by API
        else:
            print(f'Error {response.code}: {response_data}')

    # Print urllib errors
    except HTTPError as e:
        print(f'HTTPError {e.code}: {e.reason}')
    except URLError as e:
        print(f'URLError: {e.reason}')
