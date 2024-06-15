"""account command for engineai CLI."""

from typing import List

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.api import DashboardAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

ACCOUNT_ROLE = ["ADMIN", "MEMBER"]


def _show_account(accounts: List) -> None:
    """Show table for account.

    Args:
        accounts: account object list.
    """
    if accounts:
        console = Console()
        table = Table(
            title="account",
            show_header=False,
            show_edge=True,
        )
        for current_account in accounts:
            table.add_row(current_account.get("slug"))
        console.print(table)
    else:
        write_console("No account found\n", 0)


def _add_account(account_name: str) -> None:
    api = DashboardAPI()
    try:
        api.create_account(account_name)
        write_console(f"Account `{account_name}` added successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _remove_account(account_name: str) -> None:
    api = DashboardAPI()
    try:
        api.delete_account(account_name)
        write_console(f"Account `{account_name}` removed successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _update_account(account_name: str, new_account_name: str) -> None:
    api = DashboardAPI()
    try:
        api.update_account(account_name, new_account_name)
        write_console(
            f"Account `{account_name}` renamed to `{new_account_name}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _add_account_member(account_name: str, email: str, role: str) -> None:
    api = DashboardAPI()
    try:
        api.add_account_member(account_name, email, role)
        write_console(
            f"User `{email}` added to account `{account_name}` with role `{role}` "
            "successfully\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _update_account_member(account_name: str, email: str, role: str) -> None:
    api = DashboardAPI()
    try:
        api.update_account_member(account_name, email, role)
        write_console(
            f"User `{email}` updated to role `{role}` in account `{account_name}` "
            "with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _remove_account_member(account_name: str, email: str) -> None:
    api = DashboardAPI()
    try:
        api.remove_account_member(account_name, email)
        write_console(
            f"User `{email}` removed from account `{account_name}` with success\n", 0
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


def _show_account_member(accounts: List) -> None:
    if accounts:
        slug = accounts.get("slug")
        members = accounts.get("members")
        console = Console()
        table = Table(
            title=f"Members of account '{slug}'",
            show_header=False,
            show_edge=True,
        )
        for user in members:
            table.add_row(user.get("user").get("email"), user.get("role"))
        console.print(table)
    else:
        write_console("No account member found\n", 0)


def _transfer_account(account_name: str, email: str):
    api = DashboardAPI()
    try:
        api.transfer_account(account_name, email)
        write_console(
            f"Account `{account_name}` transferred to user `{email}` with success\n", 0
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@click.group(name="account", invoke_without_command=False)
def account() -> None:
    """Account commands."""


@account.command()
def ls() -> None:
    """List all account."""
    api = DashboardAPI()
    try:
        account_list = api.list_account()
        _show_account(account_list)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@account.command("add")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
def add_account(account_name: str) -> None:
    """Add new account.

    Args:
        account_name: account to be added.
    """
    _add_account(account_name)


@account.command("rm")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
def remove_account(account_name: str) -> None:
    """Remove account.

    Args:
        account_name: account to be removed.
    """
    _remove_account(account_name)


@account.command("rename")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
@click.argument(
    "new_account_name",
    required=True,
    type=str,
)
def update(account_name: str, new_account_name: str) -> None:
    """Update current account.

    Args:
        account_name: account to be updated.
        new_account_name: new account name.
    """
    _update_account(account_name, new_account_name)


@click.group()
def member():
    """Account member commands."""


@member.command("add")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(ACCOUNT_ROLE, case_sensitive=False),
)
def add_account_member(account_name: str, email: str, role: str) -> None:
    """Add new member to account.

    Args:
        account_name: account to be updated.
        email: user to be added to account.
        role: role for the user in the account (ADMIN or MEMBER).
    """
    _add_account_member(account_name, email, role.upper())


@member.command("update")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(ACCOUNT_ROLE, case_sensitive=False),
)
def update_account_member_role(account_name: str, email: str, role: str) -> None:
    """Update member role in account.

    Args:
        account_name: account to be updated.
        email: user to be updated in the account.
        role: new role for the user in the account (ADMIN or MEMBER).
    """
    _update_account_member(account_name, email, role.upper())


@member.command("rm")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def remove_account_member(account_name: str, email: str) -> None:
    """Remove member from account.

    Args:
        account_name: account to be updated.
        email: user to be removed from account.
    """
    _remove_account_member(account_name, email)


@member.command("ls")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
def ls_account_member(account_name: str) -> None:
    """List all member in account.

    Args:
        account_name: account to be selected.
    """
    api = DashboardAPI()
    try:
        accounts = api.list_account_member(account_name)
        _show_account_member(accounts)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command("transfer")
@click.argument(
    "account_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def transfer_account(account_name: str, email: str) -> None:
    """Transfer account to another member.

    Args:
        account_name: account to be updated.
        email: member to be new account owner.
    """
    _transfer_account(account_name, email)


account.add_command(member)
