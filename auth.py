from requests import Session
import hashlib
import hmac
import json

from settings import SERVER_URL, LOGIN, PASS


server_url = SERVER_URL.rstrip('/')


class ApiException(Exception):
    pass


def hash_token(username, password, token):
    sha_password = hashlib.sha512(password.encode()).hexdigest()
    hashed_username = hmac.new(
        username.encode(),
        sha_password.encode(),
        hashlib.sha512
    ).hexdigest()
    hashed_token = hmac.new(
        bytes(hashed_username.encode()),
        bytes(token.encode()),
        hashlib.sha512
    ).hexdigest()
    return hashed_token


def log_in(username=LOGIN, password=PASS, session=None):
    if session is None:
        session = Session()

    step1_url = server_url + '/Security/Authentication'
    step1 = session.post(
        url=step1_url,
        data={
            'userName': username,
        }
    )
    try:
        step1_answer = json.loads(step1.text)
    except ValueError as e:
        raise ApiException(step1_url, step1.text, e)
    try:
        token = step1_answer['Token']
    except KeyError as e:
        raise ApiException(step1_url, step1.text, e)

    hashed_token = hash_token(username, password, token)

    step2_url = server_url + '/Security/Login'
    step2 = session.post(
        url=step2_url,
        data={
            'UserName': username,
            'Token': token,
            'HashedToken': hashed_token
        }
    )
    try:
        step2_answer = json.loads(step2.text)
        session_key = step2_answer['Session']
    except (ValueError, KeyError) as e:
        raise ApiException(step2_url, step2.text, e)
    return session_key
