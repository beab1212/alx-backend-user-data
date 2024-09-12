#!/usr/bin/env python3
"""
Main file
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """testing registration route
    """
    payload = {'email': email, 'password': password}
    response = requests.post(f'{BASE_URL}/users', data=payload)
    expected = {'email': email, 'message': 'user created'}
    assert 200 == response.status_code
    assert expected == response.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """testing login route with invalid credential
    """
    payload = {'email': email, 'password': password}
    response = requests.post(f'{BASE_URL}/sessions', data=payload)
    assert 401 == response.status_code


def log_in(email: str, password: str) -> str:
    """testing login with valid credential
    """
    payload = {'email': email, 'password': password}
    response = requests.post(f'{BASE_URL}/sessions', data=payload)
    expected = {'email': email, 'message': 'logged in'}
    assert 200 == response.status_code
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """testing profile route for unlogged user
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert 403 == response.status_code


def profile_logged(session_id: str) -> None:
    """testing profile route for logged user
    """
    cookie = dict(session_id=session_id)
    response = requests.get(f'{BASE_URL}/profile', cookies=cookie)
    expected = {'email': EMAIL}
    assert 200 == response.status_code
    assert expected == response.json()


def log_out(session_id: str) -> None:
    """testing logout route
    """
    cookie = dict(session_id=session_id)
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookie)
    assert 200 == response.status_code


def reset_password_token(email: str) -> str:
    """testing reset password route
    """
    payload = {'email': email}
    res = requests.post(f'{BASE_URL}/reset_password', data=payload)
    output = res.json()
    reset_token = output.get('reset_token')
    expect = {'email': email, 'reset_token': reset_token}

    assert res.status_code == 200
    assert output == expect
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """testing update password route
    """
    payload = {'email': email,
               'reset_token': reset_token, 'new_password': new_password}
    res = requests.put(f'{BASE}/reset_password', data=payload)
    expect = {'email': email, 'message': 'Password updated'}
    assert res.status_code == 200
    assert res.json() == expect


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
