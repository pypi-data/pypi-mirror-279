"""
  Snapend CLI commands
"""
import requests
from requests.exceptions import RequestException

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT, SNAPCTL_INPUT_ERROR, \
    SNAPCTL_SUCCESS, SNAPCTL_GAME_CREATE_ERROR, SNAPCTL_GAME_ENUMERATE_ERROR, \
    HTTP_ERROR_DUPLICATE_GAME_NAME, SNAPCTL_GAME_CREATE_DUPLICATE_NAME_ERROR
from snapctl.utils.echo import error, success
from snapctl.utils.helper import snapctl_error, snapctl_success


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
        # Validate input
        self.validate_input()

    def validate_input(self) -> None:
        """
          Validator
        """
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            snapctl_error("Missing API Key.", SNAPCTL_INPUT_ERROR)
        # Check subcommand
        if not self.subcommand in Game.SUBCOMMANDS:
            snapctl_error(
                f"Invalid command. Valid commands are {', '.join(Game.SUBCOMMANDS)}.",
                SNAPCTL_INPUT_ERROR)
        # Check sdk-download commands
        if self.subcommand == 'create':
            if self.name is None or self.name == '':
                snapctl_error("Missing game name.", SNAPCTL_INPUT_ERROR)

    def create(self) -> bool:
        """
          Create a game
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
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
                snapctl_success(
                    f"Game {self.name} create successful", progress)
            response_json = res.json()
            if "api_error_code" in response_json and "message" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_DUPLICATE_GAME_NAME:
                    snapctl_error(f"Game {self.name} already exists.",
                                  SNAPCTL_GAME_CREATE_DUPLICATE_NAME_ERROR, progress)
            snapctl_error(
                f'Server error: {response_json}', SNAPCTL_GAME_CREATE_ERROR, progress)
        except RequestException as e:
            snapctl_error(f"Exception: Unable to download the SDK {e}",
                          SNAPCTL_GAME_CREATE_ERROR, progress)
        snapctl_error('Failed to create game.',
                      SNAPCTL_GAME_CREATE_ERROR, progress)

    def enumerate(self) -> bool:
        """
          Enumerate all games
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Enumerating all your games...', total=None)
        try:
            url = f"{self.base_url}/v1/snapser-api/games"
            res = requests.get(
                url, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            response_json = res.json()
            if res.ok and 'games' in response_json:
                snapctl_success(response_json['games'], progress)
            snapctl_error('Unable to enumerate games.',
                          SNAPCTL_GAME_ENUMERATE_ERROR, progress)
        except RequestException as e:
            snapctl_error(f"Exception: Unable to update your snapend {e}",
                          SNAPCTL_GAME_ENUMERATE_ERROR, progress)
        snapctl_error('Failed to enumerate games.',
                      SNAPCTL_GAME_ENUMERATE_ERROR, progress)
