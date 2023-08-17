#!/usr/bin/env python3
"""Query your web server for the corresponding end-point"""
import requests

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """register user"""
    response = requests.post(f'{BASE_URL}/users',
                             data={'email':email, 'password': password})
    assert response.status_code == 200
    print(response.json())


def log_in_wrong_password(email: str, password: str) -> None:
    """Wrong password"""
    response = requests.post(f'{BASE_URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401
    print(response.text)


def log_in(email: str, password: str) -> str:
    """Log in session"""
    response = requests.post(f'{BASE_URL}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    print(response.json())
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test user's profile unlogged"""
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403
    print(response.text)


def profile_logged(session_id: str) -> None:
    """Validate user's profile logged in"""
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.get(f'{BASE_URL}/profile', headers=headers)
    assert response.status_code == 200
    print(response.json())


def log_out(session_id: str) -> None:
    """Validate log out route handler"""
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.delete(f'{BASE_URL}/sessions', headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    return data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Validate update password route handler"""
    response = requests.post(f'{BASE_URL}/update_password',
                             data={'email': email, 'reset_token': reset_token,
                             'new_password': new_password})
    assert response.status_code == 200
    print('Password updated')


if __name__ == '__main__':
    register_user('test@test.com', 'SuperSecretPwd')

    log_in_wrong_password('test@test.com', 'WrongPwd')

    session_id = log_in('test@test.com', 'SuperSecretPwd')

    profile_unlogged()

    profile_logged(session_id)

    log_out(session_id)

    reset_token = reset_password_token('test@test.com')

    update_password('test@test.com', reset_token, 'NewSuperSecretPwd')
