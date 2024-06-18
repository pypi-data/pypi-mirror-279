import argparse
from importlib.metadata import version
import logging
import pathlib
import sys
import typing

from ..http import (
    BearerTokenDecorator,
    HttpClient,
    LocalAuthDecorator,
    PATAuthDecoratorV0,
    RobotoClient,
)
from ..profile import (
    MalformedProfileException,
    MissingProfileException,
    RobotoProfile,
)
from .actions import (
    command_set as actions_command_set,
)
from .argparse import (
    DeprecationAction,
    SortingHelpFormatter,
)
from .collections import (
    command_set as collections_command_set,
)
from .config import check_last_update
from .context import CLIContext
from .datasets import (
    command_set as datasets_command_set,
)
from .extension import (
    apply_roboto_cli_command_extensions,
    apply_roboto_cli_context_extensions,
)
from .feature_flags import get_flags_config
from .images import (
    command_set as images_command_set,
)
from .invocations import (
    command_set as invocations_command_set,
)
from .orgs import command_set as orgs_command_set
from .tokens import (
    command_set as tokens_command_set,
)
from .triggers import (
    command_set as triggers_command_set,
)
from .users import (
    command_set as users_command_set,
)

COMMAND_SETS = [
    actions_command_set,
    collections_command_set,
    datasets_command_set,
    images_command_set,
    invocations_command_set,
    orgs_command_set,
    users_command_set,
    tokens_command_set,
    triggers_command_set,
]

BETA_USER_POOL_CLIENT_ID = "7p2e45lijin58tuaairtflf3m8"
PROD_USER_POOL_CLIENT_ID = "1gricmdmh0vv582qdd84phab5"


PROGRAMMATIC_ACCESS_BLURB = (
    "To resolve this, please consult the getting started page for programmatic access at "
    + "https://docs.roboto.ai/getting-started/programmatic-access.html."
)


def __populate_context(profile: RobotoProfile, context: CLIContext):
    profile_entry = profile.get_entry()

    context.feature_flags = get_flags_config(profile.config_dir)

    http_client_args: dict[str, typing.Any] = {
        "default_endpoint": profile_entry.default_endpoint
    }

    if "localhost" in profile_entry.default_endpoint:
        http_client_args["default_auth"] = LocalAuthDecorator(
            user_id=profile_entry.user_id
        )
    elif profile_entry.token.startswith("robo_pat"):
        http_client_args["default_auth"] = PATAuthDecoratorV0.for_client(
            client_id=profile_entry.default_client_id, profile=profile
        )
    else:
        http_client_args["default_auth"] = BearerTokenDecorator(profile_entry.token)

    http = HttpClient(**http_client_args)  # type: ignore[arg-type]

    context.roboto_service_base_url = profile_entry.default_endpoint
    context.http_client = http
    context.roboto_client = RobotoClient(
        endpoint=profile_entry.default_endpoint,
        auth_decorator=http_client_args["default_auth"],
    )

    context.extensions = {}


def construct_parser(
    context: typing.Optional[CLIContext] = None,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="roboto",
        description=(
            "CLI for interacting with Roboto's Data Platform. "
            "Each of the command groups listed below have their own set of supported subcommands and help pages."
        ),
        formatter_class=SortingHelpFormatter,
    )

    parser.add_argument(
        "--debug",
        help="Deprecated. Please use the --verbose flag instead.",
        deprecation_msg="The --debug flag is deprecated. Please use the --verbose flag instead.",
        action=DeprecationAction,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        help=(
            "Set increasing levels of verbosity. "
            "By default, only ERROR logs are printed. "
            "-v prints WARNING logs, -vv prints INFO logs, -vvv prints DEBUG logs."
        ),
        action="count",
        default=0,
    )

    parser.add_argument(
        "--version",
        help="Show the version of 'roboto' currently running",
        action="store_true",
    )

    parser.add_argument(
        "--profile",
        help="Roboto profile to use; must match a section within the Roboto config.json",
        required=False,
    )

    parser.add_argument(
        "--config-file",
        help="Overrides the location of the roboto config.json file. Defaults to ~/.roboto/config.json",
        type=pathlib.Path,
        required=False,
    )

    parser.add_argument(
        "--suppress-upgrade-check",
        dest="suppress_upgrade_check",
        help="Suppresses the check for a newer 'roboto' package version.",
        action="store_true",
        required=False,
    )

    # https://bugs.python.org/issue29298
    subcommands = parser.add_subparsers(dest="function")

    for command_set in sorted(
        apply_roboto_cli_command_extensions(base_command_sets=COMMAND_SETS),
        key=lambda x: x.name,
    ):
        command_set.sort_commands()
        command_set.add_to_subparsers(subcommands, context)

    return parser


def entry():
    logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
    context = CLIContext()
    parser = construct_parser(context)
    profile = RobotoProfile()

    # By default, as soon as we figure out we're running a sub-parser, any field encountered after that subparser
    # will be ignored. This means that `roboto --debug datasets search` will work but
    # `roboto datasets search --debug` will not. In order to work around this, we can use parser_known_args,
    # which gives us back the list of un-evaluated args, and then take a second pass at parse_args with those args.
    # This will only work if our subparsers never re-define top level parameters like --debug, --config-file, etc.
    #
    # This solution was based on a stack overflow post about this issue:
    # https://stackoverflow.com/questions/46962065/add-top-level-argparse-arguments-after-subparser-args
    args, unparsed = parser.parse_known_args()
    args = parser.parse_args(unparsed, args)

    profile = (
        RobotoProfile(default_profile_name=args.profile)
        if args.config_file is None
        else RobotoProfile(
            config_file=args.config_file, default_profile_name=args.profile
        )
    )

    try:
        try:
            profile.get_entry()
        except MalformedProfileException:
            parser.error(
                f"The roboto config file located at '{profile.config_file}' is malformed. "
                + PROGRAMMATIC_ACCESS_BLURB
            )
        except MissingProfileException:
            parser.error(
                f"No roboto config file located at '{profile.config_file}'. "
                + PROGRAMMATIC_ACCESS_BLURB
            )

        __populate_context(profile, context)
        apply_roboto_cli_context_extensions(base_context=context)

        log_level = max(logging.ERROR - (args.verbose * 10), logging.DEBUG)
        logging.getLogger().setLevel(log_level)

        if args.version:
            print(version("roboto"))
        elif "func" in args:
            args.func(args)
        else:
            parser.print_help()
    finally:
        if not args.suppress_upgrade_check:
            check_last_update(profile)
