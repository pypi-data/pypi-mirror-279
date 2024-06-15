"""
    SnapCTL entrypoint
"""
import configparser
import os
from sys import platform
from typing import Union, Callable
import typer
import pyfiglet

from snapctl.commands.byosnap import ByoSnap
from snapctl.commands.byogs import ByoGs
from snapctl.commands.game import Game
from snapctl.commands.generate import Generate
from snapctl.commands.snapend import Snapend
from snapctl.config.constants import COMPANY_NAME, API_KEY, URL_KEY, CONFIG_FILE_MAC, \
    CONFIG_FILE_WIN, DEFAULT_PROFILE, VERSION, SNAPCTL_SUCCESS, SNAPCTL_ERROR, CONFIG_PATH_KEY
from snapctl.config.endpoints import END_POINTS
from snapctl.config.hashes import CLIENT_SDK_TYPES, SERVER_SDK_TYPES, PROTOS_TYPES, SERVICE_IDS, \
    SNAPEND_MANIFEST_TYPES
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info

######### Globals #########


def draw_ascii_text():
    """
      Draws the ascii text for Snapser
    """
    ascii_text = pyfiglet.figlet_format(COMPANY_NAME)
    typer.echo(ascii_text)


app = typer.Typer(
    help=draw_ascii_text(),
    context_settings={
        "help_option_names": ["-h", "--help"]
    }
)


######### HELPER METHODS #########


def extract_config(extract_key: str, profile: str | None = None) -> object:
    """
      Extracts the API Key from the environment variable and if not present from the config file
    """
    result = {
        'location': '',
        'value': None
    }
    # Option 1 - Get the API Key from the environment variable
    env_api_key = os.getenv(extract_key)
    if env_api_key is not None:
        result['location'] = 'environment-variable'
        result['value'] = env_api_key
        return result
    encoding: str | None = "utf-8-sig" if platform == 'win32' else None
    # Option 2 - Get the API Key from CONFIG PATH environment variable
    config_file_path: str | None = os.getenv(CONFIG_PATH_KEY)
    # Option 3 - Get the API Key from the hardcoded config file we look for
    if config_file_path is None:
        if platform == 'win32':
            config_file_path = os.path.expandvars(CONFIG_FILE_WIN)
        else:
            config_file_path = os.path.expanduser(CONFIG_FILE_MAC)
    result['location'] = f'config-file:{config_file_path}'
    if os.path.isfile(config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path, encoding=encoding)
        config_profile: str = DEFAULT_PROFILE
        if profile is not None and profile != '' and profile != DEFAULT_PROFILE:
            result['location'] = f'{config_file_path}:profile {profile}'
            config_profile = f'profile {profile}'
            info(f"Trying to extract API KEY from profile {profile}")
        result['value'] = config.get(
            config_profile, extract_key, fallback=None, raw=True
        )
    else:
        error(
            f'Config file on platform {platform} not found at {config_file_path}')
    return result


def get_base_url(api_key: str | None) -> str:
    """
        Returns the base url based on the api_key
    """
    # Check if the user has a URL override
    url_key_obj = extract_config(URL_KEY, None)
    if url_key_obj['value'] is not None:
        return url_key_obj['value']
    # If there was no override then we use the default
    if api_key is None:
        return ''
    if api_key.startswith('dev_'):
        return END_POINTS['DEV']
    if api_key.startswith('devtwo_'):
        return END_POINTS['DEV_TWO']
    if api_key.startswith('playtest_'):
        return END_POINTS['PLAYTEST']
    return END_POINTS['PROD']


def validate_command_context(
        ctx: typer.Context,
):
    """
      Validator to confirm if the context has been set properly
    """
    if ctx.obj['api_key'] is None or ctx.obj['base_url'] == '':
        error(
            "Unable to set command context. "
            f"API Key:{ctx.obj['api_key']}  "
            f"API Key Category:{ctx.obj['api_key_location']} "
            f"Base URL:{ctx.obj['base_url']}"
        )
        raise typer.Exit(SNAPCTL_ERROR)
    info(f"Using API Key from {ctx.obj['api_key_location']}")

######### CALLBACKS #########


def default_context_callback(ctx: typer.Context):
    """
      Common Callback to set the main app context
      This gets called on every command right at the start
    """
    # info("In default callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    # Extract the api_key
    api_key_obj = extract_config(API_KEY, None)
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


def api_key_context_callback(
        ctx: typer.Context,
        api_key: str | None = None
):
    """
      Callback to set the context for the api_key
      This gets called only if the user has added a --api-key override
    """
    if api_key is None:
        return None
    # info("In API Key callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key
    ctx.obj['api_key_location'] = 'command-line-argument'
    ctx.obj['base_url'] = get_base_url(api_key)


def profile_context_callback(
        ctx: typer.Context,
        profile: str | None = None
):
    """
      Callback to set the context for the profile
      This gets called only if the user has added a --profile override
    """
    # Its important to early return if user has already entered API Key via command line
    if profile is None or ctx.obj['api_key_location'] == 'command-line-argument':
        return None
    # info("In Profile Callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    api_key_obj = extract_config(API_KEY, profile)
    if api_key_obj['value'] is None and profile is not None and profile != '':
        conf_file = ''
        if platform == 'win32':
            conf_file = os.path.expandvars(CONFIG_FILE_WIN)
        else:
            conf_file = os.path.expanduser(CONFIG_FILE_MAC)
        error(
            f'Invalid profile input {profile}. '
            f'Please check your snap config file at {conf_file}'
        )
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = profile if profile else DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


# Presently in typer this is the only way we can expose the `--version`
def version_callback(value: bool = True):
    """
        Prints the version and exits
    """
    if value:
        success(f"Snapctl version: {VERSION}")
        raise typer.Exit(SNAPCTL_SUCCESS)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version",
        help="Get the Snapctl version.",
        callback=version_callback
    ),
):
    """
    Snapser CLI Tool
    """
    default_context_callback(ctx)

######### TYPER COMMANDS #########


@app.command()
def validate(
    ctx: typer.Context,
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
):
    """
    Validate your Snapctl setup
    """
    validate_command_context(ctx)
    success("Setup is valid")


@app.command()
def byosnap(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOSnap Subcommands: " + ", ".join(ByoSnap.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(..., help="Snap Id. Should start with byosnap-"),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap."
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoSnap.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoSnap.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag", help=(
            "(req: build, push  publish-image and publish-version) Tag for your snap"
        )
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: build, publish-image) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # publish-version
    prefix: str = typer.Option(
        '/v1', "--prefix", help="(req: publish-version) URL Prefix for your snap"
    ),
    version: Union[str, None] = typer.Option(
        None, "--version",
        help="(req: publish-version) Snap version. Should start with v. Example vX.X.X"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    byosnap_profile: Union[str, None] = typer.Option(
        None, "--byosnap-profile", help=(
            "(req: publish-version) Path to your byosnap-profile JSON file"
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own snap commands
    """
    validate_command_context(ctx)
    byosnap_obj: ByoSnap = ByoSnap(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], sid,
        name, desc, platform_type, language, tag, path, docker_file,
        prefix, version, http_port, byosnap_profile
    )
    validate_input_response: ResponseType = byosnap_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byosnap_obj, command_method)
    if not method():
        error(f"BYOSnap {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOSnap {subcommand} complete")


@app.command()
def byogs(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOGs Subcommands: " + ", ".join(ByoGs.SUBCOMMANDS) + "."
    ),
    # sid: str = typer.Argument(
    #     ByoGs.SID,  help="Game Server Id. Should start with byogs"
    # ),
    # publish, publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag",
        help="(req: build, push, publish) Tag for your snap"
    ),
    # publish and publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: build, publish) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own game server commands
    """
    validate_command_context(ctx)
    byogs_obj: ByoGs = ByoGs(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'],
        tag, path, docker_file,
    )
    validate_input_response: ResponseType = byogs_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byogs_obj, command_method)
    if not method():
        error(f"BYOGs {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOGs {subcommand} complete")


@app.command()
def game(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Game Subcommands: " + ", ".join(Game.SUBCOMMANDS) + "."
    ),
    # name
    name: str = typer.Option(
        None, "--name",
        help=("(req: create) Name of your game: ")
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Game commands
    """
    validate_command_context(ctx)
    game_obj: Game = Game(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], name)
    validate_input_response: ResponseType = game_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(game_obj, command_method)
    if not method():
        error(f"Game {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"Game {subcommand} complete")


@app.command()
def snapend(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Snapend Subcommands: " + ", ".join(Snapend.SUBCOMMANDS) + "."
    ),
    # snapend_id: str = typer.Argument(..., help="Snapend Id"),
    snapend_id: str = typer.Option(
        None, "--snapend-id",
        help=("(req: update, download) Snapend Id")
    ),
    # enumerate
    game_id: str = typer.Option(
        None, "--game-id",
        help="(req: enumerate, clone) Game Id"
    ),
    # apply, clone
    manifest_path: str = typer.Option(
        None, "--manifest-path",
        help="(req: apply|clone) Path to the manifest file"
    ),
    # download
    category: str = typer.Option(
        None, "--category",
        help=(
            "(req: download) Category of the Download: " +
            ", ".join(Snapend.DOWNLOAD_CATEGORY) + "."
        )
    ),
    platform_type: str = typer.Option(
        None, "--type",
        help=(
            "(req: --category client-sdk|server-sdk|protos --type ) "
            "SDK Types: client-sdk(" + ", ".join(CLIENT_SDK_TYPES.keys()) +
            ") server-sdk(" + ", ".join(SERVER_SDK_TYPES.keys()) +
            ") protos(" + ", ".join(PROTOS_TYPES.keys()) + ")" +
            ") snapend-manifest(" + \
            ", ".join(SNAPEND_MANIFEST_TYPES.keys()) + ")"
        )
    ),
    protos_category: str = typer.Option(
        'messages', "--protos-category",
        help=(
            "(optional: download) Only applicable for --category protos --protos-category"
            "Protos-Category: (" + ", ".join(Snapend.PROTOS_CATEGORY) + ")"
        )
    ),
    auth_type: str = typer.Option(
        'user', "--auth-type",
        help=(
            "(optional: download) Only applicable for --category server-sdk --auth-type"
            "Auth-Types: (" + ", ".join(Snapend.AUTH_TYPES) + ")"
        )
    ),
    snaps: Union[str, None] = typer.Option(
        None, "--snaps",
        help=(
            "(optional: download) Comma separated list of snap ids to customize the "
              "SDKs, protos or admin settings. "
              "snaps(" + ", ".join(SERVICE_IDS)
        )
    ),
    # Clone
    name: Union[str, None] = typer.Option(
        None, "--name", help="(req: clone) Snapend name"),
    env: Union[str, None] = typer.Option(
        None, "--env", help=(
            "(req: clone) Snapend environment"
            "Environments: (" + ", ".join(Snapend.ENV_TYPES) + ")"
        )),
    # Download, Apply, Clone
    out_path: Union[str, None] = typer.Option(
        None, "--out-path", help="(optional: download|apply|clone) Path to save the output file"),
    # update
    byosnaps: str = typer.Option(
        None, "--byosnaps",
        help=(
            "(optional: update) Comma separated list of BYOSnap ids and versions. "
            "Eg: service-1:v1.0.0,service-2:v1.0.0"
        )
    ),
    byogs: str = typer.Option(
        None, "--byogs",
        help=(
            "(optional: update) Comma separated list of BYOGs fleet name:tags. "
            "Eg: fleet-1:service-1:v1.0.0,fleet-2:service-2:v1.0.0"
        )
    ),
    # create, update, promote, apply, clone
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: update) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Snapend commands
    """
    validate_command_context(ctx)
    snapend_obj: Snapend = Snapend(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], snapend_id,
        # Enumerate, Clone
        game_id,
        # Clone
        name, env,
        # Apply, Clone
        manifest_path,
        # Download
        category, platform_type, protos_category, auth_type, snaps,
        # Download, Apply and Clone
        out_path,
        # Update
        byosnaps, byogs, blocking
    )
    validate_input_response: ResponseType = snapend_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(snapend_obj, command_method)
    if not method():
        error(f"Snapend {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"Snapend {subcommand} complete")


@app.command()
def generate(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Generate Subcommands: " + ", ".join(Generate.SUBCOMMANDS) + "."
    ),
    # byosnap-profile
    out_path: Union[str, None] = typer.Option(
        None, "--out-path", help="(req: byosnap-profile) Path to output the byosnap profile"
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Generate files to be used by other commands
    """
    validate_command_context(ctx)
    generate_obj: Generate = Generate(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'],
        out_path,
    )
    validate_input_response: ResponseType = generate_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(generate_obj, command_method)
    if not method():
        error(f"Generate {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"Generate {subcommand} complete")
