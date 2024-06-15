"""
    Generate CLI commands
"""
import json
from sys import platform
import os
from typing import Union

from snapctl.config.hashes import BYOSNAP_TEMPLATE
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success


class Generate:
    """
        Generate CLI commands
    """
    SUBCOMMANDS = ['byosnap-profile']
    BYOSNAP_PROFILE_FN = 'snapser-byosnap-profile.json'

    def __init__(
        self, subcommand: str, base_url: str, api_key: str | None,
        out_path: Union[str, None]
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.out_path: Union[str, None] = out_path

    # Validator

    def validate_input(self) -> ResponseType:
        """
          Validator
        """
        response: ResponseType = {
            'error': True,
            'msg': '',
            'data': []
        }
        if self.subcommand in ['byosnap-profile']:
            # Check path
            if self.out_path and not os.path.isdir(self.out_path):
                response['msg'] = (
                    f"Invalid path {self.out_path}. Wont be able to "
                    "store the byosnap-profile.json file"
                )
                return response
        # Send success
        response['error'] = False
        return response

    def byosnap_profile(self) -> bool:
        """
            Generate snapser-byosnap-profile.json
        """
        file_path_symbol = '/'
        if platform == 'win32':
            file_path_symbol = '\\'
        if self.out_path is not None:
            file_save_path = f"{self.out_path}{file_path_symbol}{Generate.BYOSNAP_PROFILE_FN}"
        else:
            file_save_path = f"{os.getcwd()}{file_path_symbol}{Generate.BYOSNAP_PROFILE_FN}"
        try:
            with open(file_save_path, "w") as file:
                json.dump(BYOSNAP_TEMPLATE, file, indent=4)
                success(
                    f"{Generate.BYOSNAP_PROFILE_FN} saved at {file_save_path}"
                )
                return True
        except (IOError, OSError) as file_error:
            error(f"File error: {file_error}")
        except json.JSONDecodeError as json_error:
            error(f"JSON error: {json_error}")
        except Exception as exception_error:
            error(f"An unexpected error occurred: {exception_error}")
        return False
