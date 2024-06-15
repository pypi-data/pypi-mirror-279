"""
  BYOSnap CLI commands
"""
import base64
from binascii import Error as BinasciiError
import json
import os
import re
import subprocess
from sys import platform
from typing import Union
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.config.constants import ERROR_SERVICE_VERSION_EXISTS, ERROR_TAG_NOT_AVAILABLE, \
    ERROR_ADD_ON_NOT_ENABLED
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info
from snapctl.utils.helper import get_composite_token


class ByoSnap:
    """
      CLI commands exposed for a BYOSnap
    """
    ID_PREFIX = 'byosnap-'
    SUBCOMMANDS = [
        'build', 'push', 'upload-docs',
        'create', 'publish-image', 'publish-version',
    ]
    PLATFORMS = ['linux/arm64', 'linux/amd64']
    LANGUAGES = ['go', 'python', 'ruby', 'c#', 'c++', 'rust', 'java', 'node']
    DEFAULT_BUILD_PLATFORM = 'linux/arm64'
    SID_CHARACTER_LIMIT = 47
    TAG_CHARACTER_LIMIT = 80
    VALID_CPU_MARKS = [100, 250, 500, 750, 1000, 1500, 2000, 3000]
    VALID_MEMORY_MARKS = [0.125, 0.25, 0.5, 1, 2, 3, 4]

    def __init__(
        self, subcommand: str, base_url: str, api_key: str | None, sid: str, name: str,
        desc: str, platform_type: str, language: str, input_tag: Union[str, None],
        path: Union[str, None], dockerfile: str, prefix: str, version: Union[str, None],
        http_port: Union[int, None], byosnap_profile: Union[str, None]
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.sid: str = sid
        self.name: str = name
        self.desc: str = desc
        self.platform_type: str = platform_type
        self.language: str = language
        if subcommand != 'create':
            self.token: Union[str, None] = get_composite_token(
                base_url, api_key,
                'byosnap', {'service_id': sid}
            )
        else:
            self.token: Union[str, None] = None
        self.token_parts: Union[list, None] = ByoSnap._get_token_values(
            self.token) if self.token is not None else None
        self.input_tag: Union[str, None] = input_tag
        self.path: Union[str, None] = path
        self.dockerfile: str = dockerfile
        self.prefix: str = prefix
        self.version: Union[str, None] = version
        self.http_port: Union[int, None] = http_port
        self.byosnap_profile: Union[str, None] = byosnap_profile

    # Protected methods
    @staticmethod
    def _get_token_values(token: str) -> None | list:
        """
          Method to break open the token
        """
        try:
            input_token = base64.b64decode(token).decode('ascii')
            parts = input_token.split('|')
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            # url = self.token_parts[0]
            # web_app_token = self.token_parts[1]
            # service_id = self.token_parts[2]
            # ecr_repo_url = self.token_parts[3]
            # ecr_repo_username = self.token_parts[4]
            # ecr_repo_token = self.token_parts[5]
            # platform = self.token_parts[6]
            if len(parts) >= 3:
                return parts
        except BinasciiError:
            pass
        return None

    def _check_dependencies(self) -> bool:
        """
          Check application dependencies
        """
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
            error('Unable to initialize docker')
            return False

    def _docker_login(self) -> bool:
        """
          Docker Login
        """
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
                        f'{response.returncode} - '
                        'Unable to connect to the Snapser Container Repository. '
                        'Please confirm if docker is running or try restarting docker'
                    )
                    return False
            success('Login Successful')
            return True
        except subprocess.CalledProcessError:
            error('Unable to initialize docker')
            return False

    def _docker_build(self) -> bool:
        # Get the data
        image_tag = f'{self.sid}.{self.input_tag}'
        build_platform = ByoSnap.DEFAULT_BUILD_PLATFORM
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
        image_tag = f'{self.sid}.{self.input_tag}'
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
        """
          Push the Snap image
        """
        ecr_repo_url = self.token_parts[0]
        image_tag = f'{self.sid}.{self.input_tag}'
        full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'

        # Push the image
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description='Pushing your snap...', total=None)
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

    def _validate_byosnap_profile(self) -> bool:
        """
          Validate the BYOSnap profile
        """
        response = {
            'error': True,
            'message': ''
        }
        if not self.byosnap_profile:
            response['message'] = "Missing BYOSnap profile path"
            return response
        if not os.path.isfile(self.byosnap_profile):
            response['msg'] = (
                "Unable to find BYOSnap profile "
                F"JSON at path {self.byosnap_profile}"
            )
            return response
        with open(self.byosnap_profile, 'rb') as file:
            try:
                profile_data = json.load(file)
            except json.JSONDecodeError:
                response['message'] = (
                    'Invalid BYOSnap profile JSON. Please check the JSON structure'
                )
                return response
            if 'dev_template' not in profile_data or \
                'stage_template' not in profile_data or \
                    'prod_template' not in profile_data:
                response['message'] = (
                    'Invalid BYOSnap profile JSON. Please check the JSON structure'
                )
                return response
            for profile in ['dev_template', 'stage_template', 'prod_template']:
                if 'cpu' not in profile_data[profile] or \
                    'memory' not in profile_data[profile] or \
                        'cmd' not in profile_data[profile] or \
                        'args' not in profile_data[profile] or \
                        'env_params' not in profile_data[profile]:
                    response['message'] = (
                        'Invalid BYOSnap profile JSON. Please check the JSON structure'
                    )
                    return response
                if profile_data[profile]['cpu'] not in ByoSnap.VALID_CPU_MARKS:
                    response['message'] = (
                        'Invalid CPU value in BYOSnap profile. '
                        f'Valid values are {", ".join(ByoSnap.VALID_CPU_MARKS)}'
                    )
                    return response
                if profile_data[profile]['memory'] not in ByoSnap.VALID_MEMORY_MARKS:
                    response['message'] = (
                        'Invalid Memory value in BYOSnap profile. '
                        f'Valid values are {", ".join(ByoSnap.VALID_MEMORY_MARKS)}'
                    )
                    return response
        response['error'] = False
        return response

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
        if not self.subcommand in ByoSnap.SUBCOMMANDS:
            response['msg'] = (
                "Invalid command. Valid commands ",
                f"are {', '.join(ByoSnap.SUBCOMMANDS)}."
            )
            return response
        # Validate the SID
        if not self.sid.startswith(ByoSnap.ID_PREFIX):
            response['msg'] = f"Invalid Snap ID. Valid Snap IDs start with {ByoSnap.ID_PREFIX}."
            return response
        if len(self.sid) > ByoSnap.SID_CHARACTER_LIMIT:
            response['msg'] = (
                "Invalid Snap ID. "
                f"Snap ID should be less than {ByoSnap.SID_CHARACTER_LIMIT} characters"
            )
            return response
        # Validation for subcommands
        if self.subcommand == 'create':
            if self.name == '':
                response['msg'] = "Missing name"
                return response
            if self.language not in ByoSnap.LANGUAGES:
                response['msg'] = (
                    "Invalid language. Valid languages are "
                    f"{', '.join(ByoSnap.LANGUAGES)}."
                )
                return response
            if self.platform_type not in ByoSnap.PLATFORMS:
                response['msg'] = (
                    "Invalid platform. Valid platforms are "
                    f"{', '.join(ByoSnap.PLATFORMS)}."
                )
                return response
        else:
            # Check the token
            if self.token_parts is None:
                response['msg'] = 'Invalid token. Please reach out to your support team.'
                return response
            # Check tag
            if self.input_tag is None or len(self.input_tag.split()) > 1 or \
                    len(self.input_tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                response['msg'] = (
                    "Tag should be a single word with maximum of "
                    f"{ByoSnap.TAG_CHARACTER_LIMIT} characters"
                )
                return response
            if self.subcommand == 'build' or self.subcommand == 'publish-image':
                if not self.input_tag:
                    response['msg'] = "Missing required parameter: tag"
                    return response
                if not self.path:
                    response['msg'] = "Missing required parameter: path"
                    return response
                # Check path
                if not os.path.isfile(f"{self.path}/{self.dockerfile}"):
                    response['msg'] = f"Unable to find {self.dockerfile} at path {self.path}"
                    return response
            elif self.subcommand == 'push':
                if not self.input_tag:
                    response['msg'] = "Missing required parameter: tag"
                    return response
            elif self.subcommand == 'upload-docs':
                if self.path is None:
                    response['msg'] = "Missing required parameter: path"
                    return response
            elif self.subcommand == 'publish-version':
                if not self.prefix:
                    response['msg'] = "Missing prefix"
                    return response
                if not self.version:
                    response['msg'] = "Missing version"
                    return response
                if not self.http_port:
                    response['msg'] = "Missing Ingress HTTP Port"
                    return response
                if not self.prefix.startswith('/'):
                    response['msg'] = "Prefix should start with a forward slash (/)"
                    return response
                if self.prefix.endswith('/'):
                    response['msg'] = "Prefix should not end with a forward slash (/)"
                    return response
                pattern = r'^v\d+\.\d+\.\d+$'
                if not re.match(pattern, self.version):
                    response['msg'] = "Version should be in the format vX.X.X"
                    return response
                if not self.http_port.isdigit():
                    response['msg'] = "Ingress HTTP Port should be a number"
                    return response
                # Check byosnap_profile path
                validation_response = self._validate_byosnap_profile()
                if validation_response['error']:
                    response['msg'] = validation_response['message']
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

    def upload_docs(self) -> bool:
        '''
          Note this step is optional hence we always respond with a True
        '''
        swagger_file = f"{self.path}/swagger.json"
        readme_file = f"{self.path}/README.md"
        if os.path.isfile(swagger_file):
            # Push the swagger.json
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Uploading your API Json...', total=None)
                try:
                    attachment_file = open(swagger_file, "rb")
                    url = (
                        f"{self.base_url}/v1/snapser-api/byosnaps/"
                        f"{self.sid}/docs/{self.input_tag}/openapispec"
                    )
                    test_res = requests.post(
                        url, files={"attachment": attachment_file},
                        headers={'api-key': self.api_key},
                        timeout=SERVER_CALL_TIMEOUT
                    )
                    if test_res.ok:
                        success('Uploaded swagger.json')
                    else:
                        error('Unable to upload your swagger.json')
                except RequestException as e:
                    info(
                        f'Exception: Unable to find swagger.json at {self.path} {e}'
                    )
        else:
            info('No swagger.json found at ' + self.path +
                 '. Skipping swagger.json upload')

        # Push the README.md
        if os.path.isfile(readme_file):
            # Push the swagger.json
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description='Uploading your README...', total=None)
                try:
                    attachment_file = open(readme_file, "rb")
                    url = (
                        f"{self.base_url}/v1/snapser-api/byosnaps/"
                        f"{self.sid}/docs/{self.input_tag}/markdown"
                    )
                    test_res = requests.post(
                        url, files={"attachment": attachment_file},
                        headers={'api-key': self.api_key},
                        timeout=SERVER_CALL_TIMEOUT
                    )
                    if test_res.ok:
                        success('Uploaded README.md')
                    else:
                        error('Unable to upload your README.md')
                except RequestException as e:
                    info(
                        f'Exception: Unable to find README.md at {self.path} {str(e)}'
                    )
        else:
            info(
                f'No README.md found at {self.path}. Skipping README.md upload'
            )
        return True

    # Upper echelon commands
    def create(self) -> bool:
        """
          Creating a new snap
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description='Creating your snap...', total=None)
            try:
                payload = {
                    "service_id": self.sid,
                    "name": self.name,
                    "description": self.desc,
                    "platform": self.platform_type,
                    "language": self.language,
                }
                res = requests.post(
                    f"{self.base_url}/v1/snapser-api/byosnaps",
                    json=payload, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                if res.ok:
                    return True
                response_json = res.json()
                info(response_json)
                if "api_error_code" in response_json and "message" in response_json:
                    if response_json['api_error_code'] == ERROR_SERVICE_VERSION_EXISTS:
                        error(
                            'Version already exists. Please update your version and try again'
                        )
                    elif response_json['api_error_code'] == ERROR_TAG_NOT_AVAILABLE:
                        error('Invalid tag. Please use the correct tag')
                    elif response_json['api_error_code'] == ERROR_ADD_ON_NOT_ENABLED:
                        error(
                            'Missing Add-on. Please enable the add-on via the Snapser Web app.'
                        )
                    else:
                        error(f'Server error: {response_json["message"]}')
                else:
                    error(
                        f'Server error: {json.dumps(response_json, indent=2)}'
                    )
            except RequestException as e:
                error(f"Exception: Unable to create your snap {e}")
            return False

    def publish_image(self) -> bool:
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
            not self._docker_build() or not self._docker_tag() or not self._docker_push() or \
                not self.upload_docs():
            return False
        return True

    def publish_version(self) -> bool:
        """
          Publish the version
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Publishing your snap...', total=None)
            try:
                profile_data = {}
                profile_data['dev_template'] = None
                profile_data['stage_template'] = None
                profile_data['prod_template'] = None
                with open(self.byosnap_profile, 'rb') as file:
                    profile_data = json.load(file)
                payload = {
                    "version": self.version,
                    "image_tag": self.input_tag,
                    "base_url": f"{self.prefix}/{self.sid}",
                    "http_port": self.http_port,
                    "dev_template": profile_data['dev_template'],
                    "stage_template": profile_data['stage_template'],
                    "prod_template": profile_data['prod_template']
                }
                res = requests.post(
                    f"{self.base_url}/v1/snapser-api/byosnaps/{self.sid}/versions",
                    json=payload, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                if res.ok:
                    return True
                response_json = res.json()
                if "api_error_code" in response_json:
                    if response_json['api_error_code'] == ERROR_SERVICE_VERSION_EXISTS:
                        error(
                            'Version already exists. Please update your version and try again'
                        )
                    if response_json['api_error_code'] == ERROR_TAG_NOT_AVAILABLE:
                        error('Invalid tag. Please use the correct tag')
                else:
                    error(
                        f'Server error: {json.dumps(response_json, indent=2)}'
                    )
            except RequestException as e:
                error(
                    f'Exception: Unable to publish a version for your snap {e}'
                )
            return False
