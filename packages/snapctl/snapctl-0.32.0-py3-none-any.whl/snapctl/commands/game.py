"""
  Snapend CLI commands
"""
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success


class Game:
    """
      CLI commands exposed for a Game
    """
    SUBCOMMANDS = ['create', 'enumerate']

    def __init__(
            self, subcommand: str, base_url: str, api_key: str | None, name: str | None
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.name: str | None = name

    def validate_input(self) -> ResponseType:
        """
          Validator
        """
        response: ResponseType = {
            'error': True,
            'msg': '',
            'data': []
        }
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            response['msg'] = "Missing API Key."
            return response
        # Check subcommand
        if not self.subcommand in Game.SUBCOMMANDS:
            response['msg'] = \
                f"Invalid command. Valid commands are {', '.join(Game.SUBCOMMANDS)}."
            return response
        # Check sdk-download commands
        if self.subcommand == 'create':
            if self.name is None or self.name == '':
                response['msg'] = "Missing game name."
                return response
        # Send success
        response['error'] = False
        return response

    def create(self) -> bool:
        """
          Create a game
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Creating a new game on Snapser...', total=None)
            try:
                url = f"{self.base_url}/v1/snapser-api/games"
                payload = {
                    'name': self.name
                }
                res = requests.post(
                    url, headers={'api-key': self.api_key},
                    json=payload, timeout=SERVER_CALL_TIMEOUT
                )
                if res.ok:
                    success(f"Game {self.name} has been created successfully.")
                    return True
                error('Unable to create a new game. Reason: ' + res.text)
            except RequestException as e:
                error(f"Exception: Unable to download the SDK {e}")
            return False

    def enumerate(self) -> bool:
        """
          Enumerate all games
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Enumerating all your games...', total=None)
            try:
                url = f"{self.base_url}/v1/snapser-api/games"
                res = requests.get(
                    url, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                response_json = res.json()
                if res.ok:
                    if 'games' in response_json:
                        success(response_json['games'])
                        return True
                error(response_json)
            except RequestException as e:
                error(f"Exception: Unable to update your snapend {e}")
            return False
