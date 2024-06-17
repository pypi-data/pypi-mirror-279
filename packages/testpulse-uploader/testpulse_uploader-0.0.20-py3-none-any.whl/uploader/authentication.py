import logging

import requests

from uploader.domain import TokenVerification
from uploader.exceptions import HTTPRequestFailed
from uploader.urls import ENDPOINT_TOKENS_CHECK, TESTPULSE_API, TESTPULSE_API_STAGING
from uploader.utils import is_local_dev, is_staging

logger = logging.getLogger(__name__)


def authenticate() -> None:
    token_verifier = TokenVerification()

    payload = {
        'token': token_verifier.token
    }

    url = get_receiver_url()
    req = requests.get(url=url, params=payload)

    if req.status_code != 200:
        logger.error('The token validation request failed.')
        msg = f'The token validation request failed: {req.text}'
        raise HTTPRequestFailed(msg)

    # Maybe in the future we need to save the response somewhere.
    # json_response = req.json()


def get_receiver_url():
    url = TESTPULSE_API
    if is_local_dev():
        url = "http://127.0.0.1:8080"
    elif is_staging():
        url = TESTPULSE_API_STAGING
    url = url + ENDPOINT_TOKENS_CHECK

    return url
