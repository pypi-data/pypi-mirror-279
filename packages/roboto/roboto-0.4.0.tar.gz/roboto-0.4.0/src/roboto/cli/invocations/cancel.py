import argparse

from ...domain import actions
from ..command import RobotoCommand
from ..context import CLIContext


def cancel(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = actions.Invocation.from_id(
        args.invocation_id,
        roboto_client=context.roboto_client,
    )
    invocation.cancel()
    print("Invocation cancelled.")
    return


def cancel_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")


cancel_command = RobotoCommand(
    name="cancel",
    logic=cancel,
    setup_parser=cancel_parser,
    command_kwargs={"help": "Cancel invocation."},
)
