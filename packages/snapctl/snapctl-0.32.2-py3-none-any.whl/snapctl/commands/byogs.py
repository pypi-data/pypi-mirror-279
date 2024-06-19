"""
    BYOGS CLI commands
"""
import base64
from binascii import Error as BinasciiError
import os
import subprocess
from sys import platform
from typing import Union

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SNAPCTL_BYOGS_DEPENDENCY_MISSING, \
    SNAPCTL_BYOGS_ECR_LOGIN_ERROR, SNAPCTL_BYOGS_BUILD_ERROR, \
    SNAPCTL_BYOGS_TAG_ERROR, SNAPCTL_BYOGS_PUBLISH_ERROR, \
    SNAPCTL_BYOGS_PUBLISH_DUPLICATE_TAG_ERROR, SNAPCTL_INPUT_ERROR
from snapctl.utils.echo import error, success
from snapctl.utils.helper import get_composite_token, snapctl_error, snapctl_success


class ByoGs:
    """
        BYOGS CLI commands
    """
    SID = 'byogs'
    SUBCOMMANDS = ['publish']
    PLATFORMS = ['linux/amd64']
    LANGUAGES = ['go', 'python', 'ruby', 'c#', 'c++', 'rust', 'java', 'node']
    DEFAULT_BUILD_PLATFORM = 'linux/amd64'
    SID_CHARACTER_LIMIT = 47
    TAG_CHARACTER_LIMIT = 80

    def __init__(
        self, subcommand: str, base_url: str, api_key: str | None,
        input_tag: Union[str, None], path: Union[str, None], dockerfile: str,
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        # self.sid: str = sid
        # if subcommand == 'publish':
        #     self.sid = ByoGs.SID

        self.token: Union[str, None] = get_composite_token(
            base_url, api_key, 'byogs', {'service_id': ByoGs.SID}
        )
        self.token_parts: Union[list, None] = ByoGs._get_token_values(
            self.token) if self.token is not None else None
        self.input_tag: Union[str, None] = input_tag
        self.path: Union[str, None] = path
        self.dockerfile: str = dockerfile
        # Validate input
        self.validate_input()

    # Protected methods

    @staticmethod
    def _get_token_values(token: str) -> None | list:
        """
            Get the token values
        """
        try:
            input_token = base64.b64decode(token).decode('ascii')
            token_parts = input_token.split('|')
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            # url = self.token_parts[0]
            # web_app_token = self.token_parts[1]
            # service_id = self.token_parts[2]
            # ecr_repo_url = self.token_parts[3]
            # ecr_repo_username = self.token_parts[4]
            # ecr_repo_token = self.token_parts[5]
            # platform = self.token_parts[6]
            if len(token_parts) >= 3:
                return token_parts
        except BinasciiError:
            pass
        return None

    def _check_dependencies(self) -> None:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Checking dependencies...', total=None
        )
        try:
            # Check dependencies
            result = subprocess.run([
                "docker", "info"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not result.returncode:
                return snapctl_success('BYOGS dependencies verified', progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOGS_DEPENDENCY_MISSING, progress)
        snapctl_error('Docker not running. Please start docker.',
                      SNAPCTL_BYOGS_DEPENDENCY_MISSING, progress)

    def _docker_login(self) -> None:
        # Get the data
        ecr_repo_url = self.token_parts[0]
        ecr_repo_username = self.token_parts[1]
        ecr_repo_token = self.token_parts[2]
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Logging into Snapser Image Registry...', total=None)
        try:
            # Login to Snapser Registry
            if platform == 'win32':
                response = subprocess.run([
                    'docker', 'login', '--username', ecr_repo_username,
                    '--password', ecr_repo_token, ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f'echo "{ecr_repo_token}" | docker login '
                    f'--username {ecr_repo_username} --password-stdin {ecr_repo_url}'
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success('BYOGS ECR login successful', progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOGS_ECR_LOGIN_ERROR, progress)
        snapctl_error('BYOGS ECR login failure',
                      SNAPCTL_BYOGS_ECR_LOGIN_ERROR, progress)

    def _docker_build(self) -> None:
        # Get the data
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Building your snap...', total=None)
        try:
            image_tag = f'{ByoGs.SID}.{self.input_tag}'
            build_platform = ByoGs.DEFAULT_BUILD_PLATFORM
            if len(self.token_parts) == 4:
                build_platform = self.token_parts[3]
            # Build your snap
            docker_file_path = os.path.join(self.path, self.dockerfile)
            if platform == "win32":
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    'docker', 'build', '--platform', build_platform, '-t', image_tag,
                    '-f', docker_file_path,  self.path
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    f"docker build --platform {build_platform} -t {image_tag} "
                    f"-f {docker_file_path} {self.path}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success('BYOGS build successful', progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOGS_BUILD_ERROR, progress)
        snapctl_error('BYOGS build failure',
                      SNAPCTL_BYOGS_BUILD_ERROR, progress)

    def _docker_tag(self) -> None:
        # Get the data
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Tagging your snap...', total=None)
        try:
            ecr_repo_url = self.token_parts[0]
            image_tag = f'{ByoGs.SID}.{self.input_tag}'
            full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
            # Tag the repo
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'tag', image_tag, full_ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f"docker tag {image_tag} {full_ecr_repo_url}"
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success('BYOGS tag successful', progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOGS_TAG_ERROR, progress)
        snapctl_error('BYOGS tag failure', SNAPCTL_BYOGS_TAG_ERROR, progress)

    def _docker_push(self) -> None:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Pushing your snap...', total=None)
        try:
            ecr_repo_url = self.token_parts[0]
            image_tag = f'{ByoGs.SID}.{self.input_tag}'
            full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
            # Push the image
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'push', full_ecr_repo_url
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    f"docker push {full_ecr_repo_url}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success('BYOGS upload successful', progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOGS_PUBLISH_ERROR, progress)
        snapctl_error('BYOGS upload failure. Duplicate image error.',
                      SNAPCTL_BYOGS_PUBLISH_DUPLICATE_TAG_ERROR, progress)

    # Public methods

    # Validator
    def validate_input(self) -> None:
        """
          Validator
        """
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            snapctl_error("Missing API Key.", SNAPCTL_INPUT_ERROR)
        # Check subcommand
        if not self.subcommand in ByoGs.SUBCOMMANDS:
            snapctl_error(
                f"Invalid command. Valid commands are {', '.join(ByoGs.SUBCOMMANDS)}.",
                SNAPCTL_INPUT_ERROR)
        # Validation for subcommands
        if self.token_parts is None:
            snapctl_error('Invalid token. Please reach out to your support team',
                          SNAPCTL_INPUT_ERROR)
        # Check tag
        if self.input_tag is None:
            snapctl_error("Missing required parameter:  tag",
                          SNAPCTL_INPUT_ERROR)
        if len(self.input_tag.split()) > 1 or len(self.input_tag) > ByoGs.TAG_CHARACTER_LIMIT:
            snapctl_error(
                "Tag should be a single word with maximum of "
                f"{ByoGs.TAG_CHARACTER_LIMIT} characters",
                SNAPCTL_INPUT_ERROR
            )
        if self.subcommand in ['build', 'publish']:
            if not self.path:
                snapctl_error("Missing required parameter:  path",
                              SNAPCTL_INPUT_ERROR)
            # Check path
            if not os.path.isfile(f"{self.path}/{self.dockerfile}"):
                snapctl_error(
                    f"Unable to find {self.dockerfile} at path {self.path}", SNAPCTL_INPUT_ERROR)
        # elif self.subcommand == 'push':
        #     if not self.input_tag:
        #         error("Missing required parameter:  tag", SNAPCTL_INPUT_ERROR)
        #         raise typer.Exit(code=SNAPCTL_INPUT_ERROR)

    # CRUD methods
    def build(self) -> None:
        """
          Build the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
        """
        self._check_dependencies()
        self._docker_login()
        self._docker_build()

    def push(self) -> None:
        """
          Tag the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Tag the snap
          4. Push your snap
        """
        self._check_dependencies()
        self._docker_login()
        self._docker_tag()
        self._docker_push()

    # Upper echelon commands
    def publish(self) -> None:
        """
          Publish the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
          4. Tag the repo
          5. Push the image
          6. Upload swagger.json
        """
        self._check_dependencies()
        self._docker_login()
        self._docker_build()
        self._docker_tag()
        self._docker_push()
        snapctl_success('BYOGS publish successful')
