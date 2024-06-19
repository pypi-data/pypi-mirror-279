"""
Helper functions for snapctl
"""
import requests
import typer
from requests.exceptions import RequestException
from rich.progress import Progress
from snapctl.config.constants import HTTP_NOT_FOUND, HTTP_FORBIDDEN, HTTP_UNAUTHORIZED, \
    SERVER_CALL_TIMEOUT, SNAPCTL_CONFIGURATION_ERROR, SNAPCTL_SUCCESS
from snapctl.utils.echo import error, success


def validate_api_key(base_url: str, api_key: str | None):
    """
    This function validates the API Key
    """
    try:
        url = f"{base_url}/v1/snapser-api/games"
        res = requests.get(
            url, headers={'api-key': api_key},
            timeout=SERVER_CALL_TIMEOUT
        )
        if res.ok:
            success('API Key validated')
            return True
        if res.status_code == HTTP_NOT_FOUND:
            error('Service ID is invalid.', SNAPCTL_CONFIGURATION_ERROR)
        elif res.status_code == HTTP_UNAUTHORIZED:
            error(
                'API Key verification failed. Your API Key is either invalid or may have expired. ',
                SNAPCTL_CONFIGURATION_ERROR
            )
        elif res.status_code == HTTP_FORBIDDEN:
            error(
                'Permission denied. Your role has been revoked. Please contact your administrator.',
                SNAPCTL_CONFIGURATION_ERROR
            )
        else:
            error('Failed to validate API Key. Error:',
                  SNAPCTL_CONFIGURATION_ERROR)
    except RequestException as e:
        error(f"Exception: Unable to update your snapend {e}")
    raise typer.Exit(code=SNAPCTL_CONFIGURATION_ERROR)


def get_composite_token(base_url: str, api_key: str | None, action: str, params: object) -> str:
    """
    This function exchanges the api_key for a composite token.
    """
    if not api_key or base_url == '':
        return ''
    # Exchange the api_key for a token
    payload: object = {
        'action': action,
        'params': params
    }
    res = requests.post(f"{base_url}/v1/snapser-api/composite-token",
                        headers={'api-key': api_key}, json=payload, timeout=SERVER_CALL_TIMEOUT)
    if not res.ok:
        if res.status_code == HTTP_NOT_FOUND:
            error('Service ID is invalid.')
        elif res.status_code == HTTP_UNAUTHORIZED:
            error(
                'API Key verification failed. Your API Key is either invalid or may have expired. '
            )
        elif res.status_code == HTTP_FORBIDDEN:
            error(
                'Permission denied. Your role has been revoked. Please contact your administrator.'
            )
        else:
            error(f'Failed to validate API Key. Error: {res.text}')
        raise typer.Exit(code=SNAPCTL_CONFIGURATION_ERROR)
    success('API Key validated')
    return res.json()['token']


def snapctl_success(message: str, progress: Progress | None = None, no_exit: bool = False):
    """
    This function exits the snapctl
    """
    if progress:
        progress.stop()
    success(message)
    if not no_exit:
        raise typer.Exit(code=SNAPCTL_SUCCESS)


def snapctl_error(message: str, code: int, progress: Progress | None = None):
    """
    This function exits the snapctl
    """
    if progress:
        progress.stop()
    error(message, code)
    raise typer.Exit(code=code)
