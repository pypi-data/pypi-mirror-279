import argparse

from ...domain import actions
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def delete(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    action = actions.Action.from_name(
        name=args.action,
        owner_org_id=args.org,
        roboto_client=context.roboto_client,
    )
    action.delete()
    print(f"Deleted action '{args.action}'")


def delete_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "action",
        metavar="action_reference: <action_name>",
        help="Exact name of action to delete.",
    )
    add_org_arg(parser=parser)


delete_command = RobotoCommand(
    name="delete",
    logic=delete,
    setup_parser=delete_parser,
    command_kwargs={"help": "Delete action and all of its related subresources."},
)
