import asyncio
import dataclasses
import sys
import typing

import typer

import unico_device_setuper
from unico_device_setuper.lib import auth, cnsl, env
from unico_device_setuper.scripts import paris_source, stp

COMMANDS: dict[str, stp.Handler] = {'compile-paris-source': paris_source.compile}


@dataclasses.dataclass
class GlobalOptions:
    unitech_client_strategy: auth.ClientStrategy = auth.PICK_INTERACTIVE
    unitech_env: env.UnitechEnv | None = dataclasses.field(
        default_factory=env.UnitechEnv.get_default
    )


GLOBAL_OPTIONS = GlobalOptions()


def display_help(ctx: typer.Context):
    typer.echo(ctx.get_help())
    cnsl.print(f' [bold yellow]Version:[/] [bold]{unico_device_setuper.__version__}')
    cnsl.print()


def add_arguments(f: typing.Callable[[typer.Context], None]):
    default_unitech_env_value = typing.cast(
        typing.Any,
        GLOBAL_OPTIONS.unitech_env.value if GLOBAL_OPTIONS.unitech_env is not None else None,
    )

    def wrapper(
        ctx: typer.Context,
        *,
        unitech_client: typing.Optional[str] = None,
        unitech_env: typing.Optional[env.UnitechEnv] = default_unitech_env_value,
        version: bool = typer.Option(False, '--version'),
        help: bool = typer.Option(False, '--help'),
    ):
        if help:
            display_help(ctx)
            sys.exit()

        if version:
            cnsl.print(unico_device_setuper.__version__)
            sys.exit()

        if unitech_client is not None:
            GLOBAL_OPTIONS.unitech_client_strategy = auth.PickWithName(unitech_client)

        GLOBAL_OPTIONS.unitech_env = unitech_env
        return f(ctx)

    return wrapper


def add_commands(app: typer.Typer):
    for command, handler in COMMANDS.items():
        app.registered_commands.append(
            typer.models.CommandInfo(
                name=command,
                callback=add_arguments(
                    lambda _, handler=handler: asyncio.run(
                        stp.Setup.execute(
                            stp.Args(
                                unitech_client_strategy=GLOBAL_OPTIONS.unitech_client_strategy,
                                unitech_env=GLOBAL_OPTIONS.unitech_env,
                            ),
                            handler,
                        )
                    )
                ),
            )
        )


APP = typer.Typer(pretty_exceptions_enable=False, add_completion=False)


@APP.callback(invoke_without_command=True)
@add_arguments
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        display_help(ctx)


add_commands(APP)
