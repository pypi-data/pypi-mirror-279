"""
  Snapend CLI commands
"""
from sys import platform
from typing import Union

import os
import json
import time
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.config.hashes import CLIENT_SDK_TYPES, SERVER_SDK_TYPES, PROTOS_TYPES, \
    SNAPEND_MANIFEST_TYPES
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info


class Snapend:
    """
      CLI commands exposed for a Snapend
    """
    SUBCOMMANDS = [
        'enumerate', 'clone', 'apply',
        'download', 'update', 'state'
    ]
    DOWNLOAD_CATEGORY = [
        'client-sdk', 'server-sdk', 'protos', 'admin-settings', 'snapend-manifest'
    ]
    DOWNLOAD_TYPE_NOT_REQUIRED = ['admin-settings']
    PROTOS_CATEGORY = ['messages', 'services']
    AUTH_TYPES = ['user', 'app']
    ENV_TYPES = ['DEVELOPMENT', 'STAGING']
    BLOCKING_CALL_SLEEP = 5
    MAX_BLOCKING_RETRIES = 120

    def __init__(
        self, subcommand: str, base_url: str, api_key: str | None, snapend_id: str | None,
        # Enumerate, Clone
        game_id: str | None,
        # Clone
        name: str | None,
        env: str | None,
        # Clone, Apply, Promote
        manifest_path: str | None,
        # Download
        category: str, platform_type: str, protos_category: str, auth_type: str, snaps: str | None,
        # Clone, Apply, Promote, Download
        out_path: str | None,
        # Update
        byosnaps: str | None, byogs: str | None, blocking: bool = False
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.snapend_id: str = snapend_id
        self.game_id: str | None = game_id
        self.name: str = name
        self.env: str = env
        self.manifest_path: str | None = manifest_path
        self.manifest_file_name: str | None = Snapend._get_manifest_file_name(
            manifest_path
        )
        self.category: str = category
        self.download_types: Union[
            dict[str, dict[str, str]], None
        ] = Snapend._make_download_type(category)
        self.protos_category: str = protos_category
        self.auth_type: str = auth_type
        self.platform_type: str = platform_type
        self.out_path: str | None = out_path
        self.snaps: str | None = snaps
        self.byosnap_list: Union[list, None] = Snapend._make_byosnap_list(
            byosnaps) if byosnaps else None
        self.byogs_list: str | None = Snapend._make_byogs_list(
            byogs) if byogs else None
        self.blocking: bool = blocking

    @staticmethod
    def _get_manifest_file_name(manifest_path: str) -> str | None:
        if manifest_path and manifest_path != '' and os.path.isfile(manifest_path):
            file_name = os.path.basename(manifest_path)
            if file_name.endswith('.json') or file_name.endswith('.yml') or \
                    file_name.endswith('.yaml'):
                return file_name
        return None

    @staticmethod
    def _make_download_type(category: str):
        if category == 'client-sdk':
            return CLIENT_SDK_TYPES
        if category == 'server-sdk':
            return SERVER_SDK_TYPES
        if category == 'protos':
            return PROTOS_TYPES
        if category == 'snapend-manifest':
            return SNAPEND_MANIFEST_TYPES
        return None

    @staticmethod
    def _make_byosnap_list(byosnaps: str) -> list:
        byosnap_list = []
        for byosnap in byosnaps.split(','):
            byosnap = byosnap.strip()
            if len(byosnap.split(':')) != 2:
                return []
            byosnap_list.append({
                'service_id': byosnap.split(':')[0],
                'service_version': byosnap.split(':')[1]
            })
        return byosnap_list

    @staticmethod
    def _make_byogs_list(byogs: str) -> list:
        byogs_list = []
        for byog in byogs.split(','):
            byog = byog.strip()
            if len(byog.split(':')) != 2:
                return []
            byogs_list.append({
                'fleet_name': byog.split(':')[0],
                'image_tag': byog.split(':')[1],
            })
        return byogs_list

    def _get_snapend_state(self) -> str:
        try:
            url = f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}"
            res = requests.get(
                url, headers={'api-key': self.api_key}, timeout=SERVER_CALL_TIMEOUT
            )
            cluster_object = res.json()
            if 'cluster' in cluster_object and 'id' in cluster_object['cluster'] and \
                    cluster_object['cluster']['id'] == self.snapend_id and \
                    'state' in cluster_object['cluster']:
                return cluster_object['cluster']['state']
        except RequestException as e:
            error(f"Exception: Unable to get Snapend state {e}")
        return 'INVALID'

    def _blocking_get_status(self) -> bool:
        total_tries = 0
        while True:
            total_tries += 1
            if total_tries > Snapend.MAX_BLOCKING_RETRIES:
                error("Going past maximum tries. Exiting...")
                return False
            current_state = self._get_snapend_state()
            if current_state != 'IN_PROGRESS':
                if current_state == 'LIVE':
                    success('Updated your snapend. Your snapend is Live.')
                    return True
                error(
                    f"Update not completed successfully. Your Snapend status is {current_state}.")
                return False
            info(f'Current snapend state is {current_state}')
            info(f"Retrying in {Snapend.BLOCKING_CALL_SLEEP} seconds...")
            time.sleep(Snapend.BLOCKING_CALL_SLEEP)

    def _assign_snapend_id(self, snapend_id: str) -> None:
        self.snapend_id = snapend_id

    def _setup_for_download(self, platform_type: str) -> bool:
        '''
            Called by subcommands that want to initiate a download of the new manifest post update
        '''
        download_category: str = 'snapend-manifest'
        self.category = download_category
        self.platform_type = platform_type
        self.download_types: Union[
            dict[str, dict[str, str]], None
        ] = Snapend._make_download_type(download_category)

    def _execute_download(self) -> bool:
        try:
            url = (
                f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}/"
                f"download?category={self.category}"
            )
            if self.category not in Snapend.DOWNLOAD_TYPE_NOT_REQUIRED:
                url += f"&type={self.download_types[self.platform_type]['type']}"
            # If Protos, add protos category
            if self.category == 'protos':
                url += f"&subtype={self.protos_category}"
            # If client or server SDK, add sub type and auth type
            if self.category in ['client-sdk', 'server-sdk']:
                url += f"&subtype={self.download_types[self.platform_type]['subtype']}"
                url_auth_type: str = 'user'
                if self.category == 'server-sdk' and self.auth_type == 'app':
                    url_auth_type = 'app'
                url += f"&auth_type={url_auth_type}"
            # Customize snaps
            if self.snaps:
                url += f"&snaps={self.snaps}"
            res = requests.get(
                url, headers={'api-key': self.api_key}, timeout=SERVER_CALL_TIMEOUT
            )
            fn: str = ''
            if self.category == 'admin-settings':
                fn = f"snapser-{self.snapend_id}-admin-settings.json"
            elif self.category == 'snapend-manifest':
                fn = (
                    f"snapser-{self.snapend_id}-"
                    f"manifest.{self.download_types[self.platform_type]['type']}"
                )
            elif self.category == 'protos':
                fn = (
                    f"snapser-{self.snapend_id}-{self.category}"
                    f"-{self.platform_type}-{self.protos_category}.zip"
                )
            else:
                fn = (
                    f"snapser-{self.snapend_id}-{self.category}"
                    f"-{self.platform_type}-{self.auth_type}.zip"
                )
            file_path_symbol = '/'
            if platform == 'win32':
                file_path_symbol = '\\'
            if self.out_path is not None:
                file_save_path = f"{self.out_path}{file_path_symbol}{fn}"
            else:
                file_save_path = f"{os.getcwd()}{file_path_symbol}{fn}"
            if res.ok:
                content: bytes = res.content
                with open(file_save_path, "wb") as file:
                    if self.category in ['admin-settings']:
                        content = json.loads(res.content)
                        json.dump(content, file, indent=4)
                    else:
                        file.write(res.content)
                success(f"{self.category} saved at {file_save_path}")
                return True
            error(f'Unable to download {self.category}')
        except RequestException as e:
            error(
                f"Exception: Unable to download {self.category}. Reason: {e}"
            )
        return False

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
        if not self.subcommand in Snapend.SUBCOMMANDS:
            response['msg'] = \
                f"Invalid command. Valid commands are {', '.join(Snapend.SUBCOMMANDS)}."
            return response
        if self.subcommand == 'enumerate':
            if not self.game_id:
                response['msg'] = "Missing required parameter: game_id"
                return response
        elif self.subcommand == 'clone':
            if not self.game_id:
                response['msg'] = "Missing required parameter: game_id"
                return response
            if not self.name:
                response['msg'] = "Missing required parameter: name"
                return response
            if self.env.upper() not in Snapend.ENV_TYPES:
                response['msg'] = (
                    "Invalid environment. Valid environments are "
                    f"{', '.join(Snapend.ENV_TYPES)}."
                )
                return response
            if not self.manifest_path:
                response['msg'] = "Missing required parameter: manifest_path"
                return response
        elif self.subcommand == 'apply':
            if not self.manifest_path:
                response['msg'] = "Missing required parameter: manifest_path"
                return response
            if not self.manifest_file_name:
                response['msg'] = "Invalid manifest file. Supported formats are .json, .yml, .yaml"
                return response
        elif self.subcommand == 'download':
            if self.category not in Snapend.DOWNLOAD_CATEGORY:
                response['msg'] = (
                    "Invalid SDK category. Valid categories are "
                    f"{', '.join(Snapend.DOWNLOAD_CATEGORY)}."
                )
                return response
            if self.category not in Snapend.DOWNLOAD_TYPE_NOT_REQUIRED and \
                    (self.download_types is None or self.platform_type not in self.download_types):
                response['msg'] = "Invalid Download type."
                return response
            # Check file path
            if self.out_path and not os.path.isdir(f"{self.out_path}"):
                response['msg'] = (
                    f"Invalid path {self.out_path}. "
                    "Please enter a valid path to save your output file"
                )
                return response
            # Check the Protos category
            if self.category == 'protos' and self.protos_category not in Snapend.PROTOS_CATEGORY:
                response['msg'] = (
                    "Invalid Protos category. Valid categories are "
                    f"{', '.join(Snapend.PROTOS_CATEGORY)}."
                )
                return response
            # Check the auth type
            if self.category == 'server-sdk' and self.auth_type not in Snapend.AUTH_TYPES:
                response['msg'] = (
                    "Invalid auth type. Valid auth types are "
                    f"{', '.join(Snapend.AUTH_TYPES)}."
                )
                return response
        elif self.subcommand == 'promote':
            if not self.snapend_id:
                response['msg'] = "Missing required parameter: snapend_id"
                return response
        # Check update commands
        elif self.subcommand == 'update':
            byosnap_present = True
            if self.byosnap_list is None or len(self.byosnap_list) == 0:
                byosnap_present = False
            byogs_present = True
            if self.byogs_list is None or len(self.byogs_list) == 0:
                byogs_present = False
            if not byosnap_present and not byogs_present:
                response['msg'] = "The update command needs one of byosnaps or byogs"
                return response
        # Send success
        response['error'] = False
        return response

    ## Subcommands ##
    def enumerate(self) -> bool:
        """
          List Snapends
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Enumerating all your game snapends...', total=None)
            try:
                url = f"{self.base_url}/v1/snapser-api/snapends?game_id={self.game_id}"
                res = requests.get(
                    url, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                response_json = res.json()
                if res.ok:
                    if 'clusters' in response_json:
                        success(response_json['clusters'])
                        return True
                error(response_json)
            except RequestException as e:
                error(f"Exception: Unable to update your snapend {e}")
            return False

    def clone(self) -> bool:
        """
          Create a Snapend from a manifest
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Applying your manifest...', total=None)
            try:
                with open(self.manifest_path, 'rb') as file:
                    files = {'snapend-manifest': file}
                    payload = {
                        'game_id': self.game_id,
                        'name': self.name,
                        'env': self.env.upper(),
                        'ext': self.manifest_file_name.split('.')[-1]
                    }
                    url = f"{self.base_url}/v1/snapser-api/snapends/snapend-manifest"
                    res = requests.post(
                        url, headers={'api-key': self.api_key},
                        files=files, data=payload, timeout=SERVER_CALL_TIMEOUT
                    )
                    if res.ok:
                        # extract the cluster ID
                        response = res.json()
                        if 'cluster' not in response or 'id' not in response['cluster']:
                            error(
                                'Something went wrong. Please try again in sometime.'
                            )
                            return False
                        self._assign_snapend_id(response['cluster']['id'])
                        info(
                            f"Cluster ID assigned: {response['cluster']['id']}")
                        if self.blocking:
                            status = self._blocking_get_status()
                            # Fetch the new manifest
                            if status is True:
                                # TODO: Uncomment this if we want to do an auto download
                                # self._setup_for_download(
                                #     self.manifest_file_name.split('.')[-1])
                                # self._execute_download()
                                info(
                                    'Do not forget to download the latest manifest.'
                                )
                                return True
                            info(
                                'Snapend clone has been initiated but the Snapend is not up yet.'
                                'Please try checking the status of the Snapend in some time'
                            )
                            return False
                        info(
                            "Snapend clone has been initiated. "
                            "You can check the status using "
                            f"`snapctl snapend state --snapend-id {response['cluster']['id']}`"
                        )
                        return True
                    error('Unable to apply the manifest. Reason: ' + res.text)
            except RequestException as e:
                error(f"Exception: Unable to apply the manifest snapend {e}")
            return False

    def apply(self) -> bool:
        """
          Apply a manifest
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Applying your manifest...', total=None)
            try:
                with open(self.manifest_path, 'rb') as file:
                    files = {'snapend-manifest': file}
                    payload = {
                        'ext': self.manifest_file_name.split('.')[-1]
                    }
                    url = f"{self.base_url}/v1/snapser-api/snapends/snapend-manifest"
                    res = requests.put(
                        url, headers={'api-key': self.api_key},
                        files=files, data=payload, timeout=SERVER_CALL_TIMEOUT
                    )
                    if res.ok:
                        # extract the cluster ID
                        response = res.json()
                        if 'cluster' not in response or 'id' not in response['cluster']:
                            error(
                                'Something went wrong. Please try again in sometime.'
                            )
                            return False
                        self._assign_snapend_id(response['cluster']['id'])
                        if self.blocking:
                            status = self._blocking_get_status()
                            # Fetch the new manifest
                            if status is True:
                                # TODO: Uncomment this if we want to do an auto download
                                # self._setup_for_download(
                                #     self.manifest_file_name.split('.')[-1])
                                # self._execute_download()
                                info(
                                    'Do not forget to download the latest manifest.'
                                )
                                return True
                            info(
                                'Snapend apply has been initiated but the Snapend is not up yet.'
                                'Please try checking the status of the Snapend in some time'
                            )
                            return False
                        info(
                            "Snapend apply has been initiated. "
                            "You can check the status using "
                            f"`snapctl snapend state --snapend-id {response['cluster']['id']}`"
                        )
                        return True
                    error('Unable to apply the manifest. Reason: ' + res.text)
            except RequestException as e:
                error(f"Exception: Unable to apply the manifest snapend {e}")
            return False

    def promote(self) -> bool:
        """
          Promote a staging manifest to production
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Promoting your staging snapend...', total=None)
            try:
                with open(self.manifest_path, 'rb') as file:
                    payload = {
                        'snapend_id': self.snapend_id
                    }
                    url = f"{self.base_url}/v1/snapser-api/snapends/promote"
                    res = requests.put(
                        url, headers={'api-key': self.api_key},
                        json=payload, timeout=SERVER_CALL_TIMEOUT
                    )
                    if res.ok:
                        # extract the cluster ID
                        response = res.json()
                        if 'cluster' not in response or 'id' not in response['cluster']:
                            error(
                                'Something went wrong. Please try again in sometime.'
                            )
                            return False
                        self._assign_snapend_id(response['cluster']['id'])
                        if self.blocking:
                            status = self._blocking_get_status()
                            if status is True:
                                # TODO: Uncomment this if we want to do an auto download
                                # self._setup_for_download(
                                #     self.manifest_file_name.split('.')[-1])
                                # self._execute_download()
                                # Fetch the new manifest
                                info(
                                    'Do not forget to download the latest manifest.'
                                )
                                return True
                            info(
                                'Snapend apply has been initiated but the Snapend is not up yet.'
                                'Please try checking the status of the Snapend in some time'
                            )
                            return False
                        info(
                            "Snapend apply has been initiated. "
                            "You can check the status using "
                            f"`snapctl snapend state --snapend-id {response['cluster']['id']}`"
                        )
                        return True
                    error('Unable to promote the manifest. Reason: ' + res.text)
            except RequestException as e:
                error(f"Exception: Unable to apply the manifest snapend {e}")
            return False

    def download(self) -> bool:
        """
          Download SDKs, Protos, Admin Settings and Configuration
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f'Downloading your Custom {self.category}...', total=None)
            return self._execute_download()

    def update(self) -> bool:
        """
          Update a Snapend
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Updating your Snapend...', total=None)
            try:
                payload = {
                    'byosnap_updates': self.byosnap_list,
                    'byogs_updates': self.byogs_list
                }
                url = f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}"
                res = requests.patch(
                    url, json=payload, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                if res.ok:
                    if self.blocking:
                        return self._blocking_get_status()
                    success(
                        'Snapend update has been initiated. '
                        'You can check the status using `snapctl snapend state`'
                    )
                    return True
                response_json = res.json()
                error(response_json['details'][0])
            except RequestException as e:
                error(f"Exception: Unable to update your snapend {e}")
            return False

    def state(self) -> bool:
        """
          Get the state of a Snapend
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Getting your Snapend state...', total=None)
            current_state = self._get_snapend_state()
            if current_state != 'INVALID':
                success('Current snapend state is: ' + current_state)
                return True
            error("Unable to get the snapend state.")
            return False
