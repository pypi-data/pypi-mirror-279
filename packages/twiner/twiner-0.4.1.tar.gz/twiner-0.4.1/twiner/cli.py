from datetime import timedelta
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from typing_extensions import Annotated

from twiner import __appname__, __version__
from twiner.config import TwinerConfig
from twiner.notify import send_notify
from twiner.twitch import Twitch

app = typer.Typer(help="🎮 Twiner CLI (Twitch Notifier)")
console = Console()


def version_cb(value: bool):
    """Callback that shows the current version."""

    if value:
        console.print(__appname__, __version__)
        raise typer.Exit(0)


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            "-V",
            help="Show the current version.",
            is_flag=True,
            callback=version_cb,
        ),
    ] = False
):
    """Configure a callback to print version number."""


@app.command()
def add(
    user: Annotated[str, typer.Argument(..., help="Username from Twitch.")],
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH,
):
    """Add a user to the notification pool."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        twitch = Twitch(config)

        if twitch.is_api_working():
            if twitch.is_user_valid(user):
                config.yaml["tonotify"][user] = twitch.get_usericon(
                    config, user
                )
                config.write_to_config(config.yaml)
                console.print(
                    f"\n✅ User was added successfully at {config.path}"
                )
            else:
                console.print("❌ User is not valid! Doesn't exist on Twitch")
                raise typer.Exit(1)
        else:
            console.print("❌ Invalid credentials")
            raise typer.Exit(1)

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def remove(
    user: Annotated[str, typer.Argument(..., help="Username from Twitch.")],
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH,
):
    """Remove a user from the notification pool."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        try:
            del config.yaml["tonotify"][user]
            usericon = config.datadir / f"{user}.png"
            if usericon.exists():
                usericon.unlink()

            config.write_to_config(config.yaml)
            console.print(
                f"✅ User was removed successfully from {config.path}"
            )
        except KeyError as exc:
            raise KeyError(f"{user} doesn't exist in config file") from exc

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def configure(
    client_id: Annotated[
        str, typer.Option(..., help="Twitch Client ID.", prompt="👤 Client ID")
    ],
    client_secret: Annotated[
        str,
        typer.Option(
            ..., help="Twitch Client Secret.", prompt="🔑 Client Secret"
        ),
    ],
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH,
):
    """Configure the Twitch Credentials."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        twitch = Twitch(config)
        response = twitch.get_access_token(client_id, client_secret)

        if response.status_code == 200:
            console.print("\n✅ Access token successfully obtained")

            config.yaml["creds"]["client_id"] = client_id
            config.yaml["creds"]["client_secret"] = client_secret
            config.yaml["creds"]["access_token"] = response.json()[
                "access_token"
            ]
            config.yaml["creds"]["expires_in"] = response.json()["expires_in"]

            config.write_to_config(config.yaml)
            console.print(f"🍰 Twitch credentials was stored at {config.path}")
            console.print(response.json())
        else:
            console.print("\n❌ Couldn't obtain access token")
            console.print(response.json())
            raise typer.Exit(1)

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def start(
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH
):
    """Start the notification loop."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        twitch = Twitch(config)

        if twitch.is_api_working():
            console.print(
                Panel(
                    str([user.username for user in twitch.users]),
                    title="Users to Notify",
                    highlight=True,
                    border_style="grey42",
                    expand=False,
                )
            )

            twitch.notification_loop(config, send_notify)

        else:
            console.print("❌ Invalid credentials")
            raise typer.Exit(1)

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def refresh(
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH
):
    """Refresh the user profile pictures."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        twitch = Twitch(config)

        if twitch.is_api_working():
            for user in config.yaml["tonotify"]:
                if twitch.is_user_valid(user):
                    usericon = config.datadir / f"{user}.png"
                    if usericon.exists():
                        usericon.unlink()

                    config.yaml["tonotify"][user] = twitch.get_usericon(
                        config, user
                    )
                    config.write_to_config(config.yaml)
                else:
                    console.print(
                        f"\n❌ {user} doesn't exist anymore. Run 'twiner remove {user}'"
                    )
                    raise typer.Exit(1)

            console.print(
                f"\n✅ User data was refreshed successfully from {config.path}"
            )
        else:
            console.print("❌ Invalid credentials")
            raise typer.Exit(1)

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def list(
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH
):
    """List the config file fields."""

    try:
        config = TwinerConfig(configfile)
        config.read_from_config()

        userslist = [
            f'{user[0]} = "{user[1]}"'
            for user in config.yaml["tonotify"].items()
        ]
        userslist_message = ""

        for i, user in enumerate(userslist):
            userslist_message += f"\t[{i+1}] {user}\n"

        message = (
            "[b]Geral[/]:\n"
            f"\t[b]show_user_picture[/]: "
            f"{config.yaml['geral']['show_user_picture']}\n"
            f"\t[b]notification_timeout[/]: "
            f"{config.yaml['geral']['notification_timeout']}\n"
            f"\t[b]loop_period[/]: "
            f"{config.yaml['geral']['loop_period']}\n\n"
            "[b]Credentials[/]:\n"
            f"\t[b]Client ID[/]: "
            f"{config.yaml['creds']['client_id']}\n"
            f"\t[b]Client Secret[/]: "
            f"{config.yaml['creds']['client_secret']}\n"
            f"\t[b]Access Token[/]: "
            f"{config.yaml['creds']['access_token']}\n"
            f"\t[b]Expires in[/]: "
            f"{timedelta(seconds=config.yaml['creds']['expires_in']).days} "
            f"days ({config.yaml['creds']['expires_in']} seconds)\n\n"
            f"[b]Users to notify[/]:\n"
            f"{userslist_message}"
        )

        console.print(
            Panel(
                message,
                title=str(config.path),
                highlight=True,
                border_style="grey42",
            )
        )

    except FileNotFoundError as exc:
        raise FileNotFoundError("Run 'twiner init' first.") from exc


@app.command()
def init(
    configfile: Annotated[
        Optional[str],
        typer.Option("--config", "-c", help="Specify a custom config path."),
    ] = TwinerConfig.DEFAULT_CONFIG_PATH
):
    """Init the config file (it will perform a redefining action through
    the config file, using it exclusively for the initial setup)."""

    config = TwinerConfig(configfile)

    if not config.path.exists():
        console.print(
            f"[b]✅ Config file was successfully created at {config.path}[/]"
        )
    else:
        console.print(
            f"[b]❎ Config file already exists at {config.path} (overwriting current file)[/]"
        )

    config.write_to_config(config.template)
