"""
    Generate CLI commands
"""
import json
import os
from typing import Union
from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SNAPCTL_INPUT_ERROR, \
    SNAPCTL_GENERATE_GENERIC_ERROR
from snapctl.config.hashes import BYOSNAP_TEMPLATE
from snapctl.utils.echo import error
from snapctl.utils.helper import snapctl_error, snapctl_success


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
        # Validate input
        self.validate_input()

    # Validator

    def validate_input(self) -> None:
        """
          Validator
        """
        if self.subcommand not in Generate.SUBCOMMANDS:
            snapctl_error(
                f"Invalid command {self.subcommand}. Valid command are "
                f"{Generate.SUBCOMMANDS}",
                SNAPCTL_INPUT_ERROR
            )
        if self.subcommand in ['byosnap-profile']:
            # Check path
            if self.out_path and not os.path.isdir(self.out_path):
                snapctl_error(
                    f"Invalid path {self.out_path}. Wont be able to "
                    "store the byosnap-profile.json file",
                    SNAPCTL_INPUT_ERROR
                )

    def byosnap_profile(self) -> None:
        """
            Generate snapser-byosnap-profile.json
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Promoting your staging snapend...', total=None)
        try:
            if self.out_path is not None:
                file_save_path = os.path.join(
                    self.out_path, Generate.BYOSNAP_PROFILE_FN)
            else:
                file_save_path = os.path.join(
                    os.getcwd(), Generate.BYOSNAP_PROFILE_FN)
            file_written = False
            with open(file_save_path, "w") as file:
                json.dump(BYOSNAP_TEMPLATE, file, indent=4)
                file_written = True
            if file_written:
                snapctl_success(
                    "BYOSNAP Profile generation successful. "
                    f"{Generate.BYOSNAP_PROFILE_FN} saved at {file_save_path}",
                    progress
                )
        except (IOError, OSError) as file_error:
            snapctl_error(f"File error: {file_error}",
                          SNAPCTL_GENERATE_GENERIC_ERROR, progress)
        except json.JSONDecodeError as json_error:
            snapctl_error(f"JSON error: {json_error}",
                          SNAPCTL_GENERATE_GENERIC_ERROR, progress)
        snapctl_error(
            "Failed to generate BYOSNAP Profile",
            SNAPCTL_GENERATE_GENERIC_ERROR,
            progress
        )
