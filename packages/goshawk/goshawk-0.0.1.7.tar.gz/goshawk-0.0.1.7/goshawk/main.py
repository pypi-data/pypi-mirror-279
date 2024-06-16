import importlib.metadata
from typing import List, Optional

import typer
from typing_extensions import Annotated

import goshawk.domain as domain
from goshawk.controller.deploy import clone_database
from goshawk.logging import LOG
from goshawk.visuals.view_tree import view_tree

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def main(version: bool = False) -> None:
    """
    Output the version #
    """
    LOG.debug("In callback")

    if version:
        print(importlib.metadata.metadata("goshawk")["Version"])


@app.command()
def view_model_tree(
    ctx: typer.Context,
    mask: Annotated[
        Optional[List[str]],
        typer.Option(help="Mask to deploy"),
    ] = None,
    schemas_only: Annotated[bool, typer.Option("--schemas-only")] = False,
    dry_run: Annotated[Optional[bool], typer.Option(help="No URL will be opened")] = False,
) -> None:
    LOG.debug("view model tree")
    LOG.debug(f"parms {ctx.params}")
    domain.cli_params = ctx.params
    domain.models.cli_params = ctx.params
    view_tree(mask)
    # domain.models.clear_state()
    # if schemas_only:
    #    vst(mask)
    # else:
    #    vmt(mask)


@app.command()
def data_refresh(
    db_env: Annotated[str, typer.Option(help="Name of db environment")] = "",
    mask: Annotated[Optional[List[str]], typer.Option(help="Mask to deploy")] = None,
    #    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None,
) -> None:
    LOG.debug("Data refresh")


@app.command()
def model_deploy(
    ctx: typer.Context,
    db_env: Annotated[str, typer.Option(help="Name of db environment")] = "",
    mask: Annotated[Optional[List[str]], typer.Option(help="Mask to deploy")] = None,
    dry_run: Annotated[Optional[bool], typer.Option(help="No actual deployment")] = False,
) -> None:
    LOG.debug(f"Model deploy dbenv={db_env},mask={mask} ")
    domain.cli_params = ctx.params
    LOG.debug("Data refresh")


@app.command()
def init_env(
    ctx: typer.Context,
    db_env: Annotated[str, typer.Option(help="Name of db environment")] = "",
    mask: Annotated[Optional[List[str]], typer.Option(help="Mask to specify database if necessary")] = None,
    dry_run: Annotated[Optional[bool], typer.Option(help="No actual deployment")] = False,
) -> None:
    LOG.debug(f"Model deploy db_env={db_env},mask={mask} ")
    domain.cli_params = ctx.params
    LOG.debug(f"domain.cli_params={domain.cli_params} ")
    LOG.debug(f"ctx.params={ctx.params} ")
    clone_database()


@app.command()
def destroy_env(envname: str) -> None:
    LOG.debug(f"Destroying environment: {envname}")


if __name__ == "__main__":
    app()
