"""
    BYOGS CLI commands
"""
import base64
from binascii import Error as BinasciiError
import os
import subprocess
from sys import platform
from typing import Union

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success
from snapctl.utils.helper import get_composite_token


class ByoGs:
    """
        BYOGS CLI commands
    """
    SID = 'byogs'
    SUBCOMMANDS = ['build', 'push', 'publish']
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

    def _check_dependencies(self) -> bool:
        try:
            # Check dependencies
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Checking dependencies...', total=None)
                try:
                    subprocess.run([
                        "docker", "--version"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
                except subprocess.CalledProcessError:
                    error('Docker not present')
                    return False
            success('Dependencies Verified')
            return True
        except subprocess.CalledProcessError:
            error('CLI Error')
            return False

    def _docker_login(self) -> bool:
        # Get the data
        ecr_repo_url = self.token_parts[0]
        ecr_repo_username = self.token_parts[1]
        ecr_repo_token = self.token_parts[2]
        try:
            # Login to Snapser Registry
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Logging into Snapser Image Registry...', total=None)
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
                if response.returncode:
                    error(
                        'Unable to connect to the Snapser Container Repository. '
                        'Please confirm if docker is running or try restarting docker'
                    )
                    return False
            success('Login Successful')
            return True
        except subprocess.CalledProcessError:
            error('CLI Error')
            return False

    def _docker_build(self) -> bool:
        # Get the data
        image_tag = f'{ByoGs.SID}.{self.input_tag}'
        build_platform = ByoGs.DEFAULT_BUILD_PLATFORM
        if len(self.token_parts) == 4:
            build_platform = self.token_parts[3]
        try:
            # Build your snap
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Building your snap...', total=None)
                docker_file_path = f"{self.path}/{self.dockerfile}"
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
                        f"docker build --platform {build_platform} -t {image_tag} -f {docker_file_path} {self.path}"
                    ], shell=True, check=False)
                    # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                if response.returncode:
                    error('Unable to build docker')
                    return False
            success('Build Successful')
            return True
        except subprocess.CalledProcessError:
            error('CLI Error')
            return False

    def _docker_tag(self) -> bool:
        # Get the data
        ecr_repo_url = self.token_parts[0]
        image_tag = f'{ByoGs.SID}.{self.input_tag}'
        full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
        try:
            # Tag the repo
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Tagging your snap...', total=None)
                if platform == "win32":
                    response = subprocess.run([
                        'docker', 'tag', image_tag, full_ecr_repo_url
                    ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
                else:
                    response = subprocess.run([
                        f"docker tag {image_tag} {full_ecr_repo_url}"
                    ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
                if response.returncode:
                    error('Unable to tag your snap')
                    return False
            success('Tag Successful')
            return True
        except subprocess.CalledProcessError:
            error('CLI Error')
            return False

    def _docker_push(self) -> bool:
        try:
            ecr_repo_url = self.token_parts[0]
            image_tag = f'{ByoGs.SID}.{self.input_tag}'
            full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'

            # Push the image
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Pushing your snap...', total=None)
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
                if response.returncode:
                    error('Unable to push your snap')
                    return False
            success('Snap Upload Successful')
            return True
        except subprocess.CalledProcessError:
            error('CLI Error')
            return False

    # Public methods

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
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            response['msg'] = "Missing API Key."
            return response
        # Check subcommand
        if not self.subcommand in ByoGs.SUBCOMMANDS:
            response['msg'] = f"Invalid command. Valid commands are {', '.join(ByoGs.SUBCOMMANDS)}."
            return response
        # Validation for subcommands
        if self.token_parts is None:
            response['msg'] = 'Invalid token. Please reach out to your support team'
            return response
        # Check tag
        if self.input_tag is None or len(self.input_tag.split()) > 1 or \
                len(self.input_tag) > ByoGs.TAG_CHARACTER_LIMIT:
            response['msg'] = (
                "Tag should be a single word with maximum of "
                f"{ByoGs.TAG_CHARACTER_LIMIT} characters"
            )
            return response
        if self.subcommand in ['build', 'publish']:
            if not self.input_tag:
                response['msg'] = "Missing required parameter:  tag"
                return response
            if not self.path:
                response['msg'] = "Missing required parameter:  path"
                return response
            # Check path
            if not os.path.isfile(f"{self.path}/{self.dockerfile}"):
                response['msg'] = f"Unable to find {self.dockerfile} at path {self.path}"
                return response
        elif self.subcommand == 'push':
            if not self.input_tag:
                response['msg'] = "Missing required parameter:  tag"
                return response
        # Send success
        response['error'] = False
        return response

    # CRUD methods
    def build(self) -> bool:
        """
          Build the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
        """
        if not self._check_dependencies() or not self._docker_login() or \
                not self._docker_build():
            return False
        return True

    def push(self) -> bool:
        """
          Tag the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Tag the snap
          4. Push your snap
        """
        if not self._check_dependencies() or not self._docker_login() or \
                not self._docker_tag() or not self._docker_push():
            return False
        return True

    # Upper echelon commands
    def publish(self) -> bool:
        """
          Publish the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
          4. Tag the repo
          5. Push the image
          6. Upload swagger.json
        """
        if not self._check_dependencies() or not self._docker_login() or \
                not self._docker_build() or not self._docker_tag() or not self._docker_push():
            return False
        return True
