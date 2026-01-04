"""CLI entry point using Typer.

This module provides the steward CLI for workshop management:
- steward init: Initialize workshop directory structure
- steward intake: Move items from inbox to workshop
- steward stage: Transition items between stages
- steward sync: Regenerate symlinks from status.yaml
- steward list: List items in workshop
"""

from typing import Annotated

import typer

from steward import __version__
from steward.application import (
    init_workshop,
    intake_item,
    list_items,
    stage_item,
    sync_workshop,
)
from steward.domain import (
    AmbiguousItemError,
    ExitCode,
    InvalidStageTransitionError,
    ItemNotFoundError,
    Stage,
    WorkshopAlreadyExistsError,
    WorkshopError,
)
from steward.infrastructure import get_console, get_error_console

app = typer.Typer(
    name="steward",
    help="Workshop management for Praxis.",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console = get_console()
        console.print(f"steward {__version__}")
        raise typer.Exit(ExitCode.SUCCESS)


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
) -> None:
    """Steward - Workshop management for Praxis."""
    pass


@app.command()
def init() -> None:
    """Initialize workshop directory structure.

    Creates the _workshop/ directory structure at $PRAXIS_HOME with:
    - Stage directories (inbox, intake, backlog, forge, review, shelf)
    - Exit directories (handoff, archive, trash)
    - Canonical storage (9-items/)
    - .gitignore patterns
    """
    console = get_console()
    err_console = get_error_console()

    try:
        workshop_path = init_workshop()
        console.print(f"[green]Workshop initialized at:[/green] {workshop_path}")
        raise typer.Exit(ExitCode.SUCCESS)

    except WorkshopAlreadyExistsError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.WORKSHOP_EXISTS) from None

    except WorkshopError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ENV_ERROR) from None


@app.command()
def intake(
    source: Annotated[
        str,
        typer.Argument(help="File or folder name in inbox."),
    ],
    slug: Annotated[
        str | None,
        typer.Option(
            "--slug",
            "-s",
            help="Custom slug (otherwise derived from source name).",
        ),
    ] = None,
    move: Annotated[
        bool,
        typer.Option(
            "--move",
            "-m",
            help="Move instead of copy (removes source from inbox).",
        ),
    ] = False,
) -> None:
    """Intake an item from inbox to workshop.

    Copies (default) or moves the specified file or folder from 1-inbox/
    to 9-items/, creates status.yaml, and creates a symlink in 3-intake/.

    By default, the source is copied (preserved in inbox). Use --move to
    remove the source from inbox after intake.

    Examples:
        steward intake my-idea.md
        steward intake my-folder/
        steward intake "My Project" --slug my-project
        steward intake my-idea.md --move
    """
    console = get_console()
    err_console = get_error_console()

    try:
        item = intake_item(source, custom_slug=slug, move=move)
        action = "moved" if move else "copied"
        console.print(f"[green]Intake complete ({action}):[/green] {item.id}")
        console.print(f"  Stage: {item.stage.value}")
        console.print(f"  Path: {item.path}")
        raise typer.Exit(ExitCode.SUCCESS)

    except ItemNotFoundError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ITEM_NOT_FOUND) from None

    except WorkshopError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ENV_ERROR) from None


@app.command()
def stage(
    item_slug: Annotated[
        str,
        typer.Argument(help="Item slug or partial match."),
    ],
    to_stage: Annotated[
        str,
        typer.Argument(help="Target stage name."),
    ],
) -> None:
    """Transition an item to a new stage.

    Valid stages: inbox, intake, backlog, forge, review, shelf,
    handoff, archive, trash.

    Stage transitions follow these rules:
    - Standard: inbox -> intake -> backlog -> forge -> review
    - Fast-track: intake -> forge (skip backlog)
    - Shelving: forge <-> shelf (bidirectional)
    - Exits: ANY stage -> handoff | archive | trash

    Examples:
        steward stage my-feature backlog
        steward stage my-feature forge
        steward stage my-feature archive
    """
    console = get_console()
    err_console = get_error_console()

    try:
        item = stage_item(item_slug, to_stage)
        console.print(f"[green]Stage transition complete:[/green] {item.id}")
        console.print(f"  Stage: {item.stage.value}")
        raise typer.Exit(ExitCode.SUCCESS)

    except ItemNotFoundError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ITEM_NOT_FOUND) from None

    except AmbiguousItemError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        err_console.print("[dim]Matching items:[/dim]")
        for match in e.matches:
            err_console.print(f"  - {match}")
        raise typer.Exit(ExitCode.ITEM_NOT_FOUND) from None

    except InvalidStageTransitionError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        valid_stages = ", ".join(s.value for s in Stage)
        err_console.print(f"[dim]Valid stages: {valid_stages}[/dim]")
        raise typer.Exit(ExitCode.INVALID_TRANSITION) from None

    except WorkshopError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ENV_ERROR) from None


@app.command()
def sync() -> None:
    """Regenerate all symlinks from status.yaml files.

    Clears all existing symlinks in stage folders and recreates them
    based on the stage field in each item's status.yaml.

    Use this command to fix broken symlinks or after manual edits
    to status.yaml files.

    Examples:
        steward sync
    """
    console = get_console()
    err_console = get_error_console()

    try:
        created, removed = sync_workshop()
        console.print("[green]Sync complete[/green]")
        console.print(f"  Symlinks created: {created}")
        console.print(f"  Orphans removed: {removed}")
        raise typer.Exit(ExitCode.SUCCESS)

    except WorkshopError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ENV_ERROR) from None


@app.command(name="list")
def list_cmd(
    stage_filter: Annotated[
        str | None,
        typer.Option(
            "--stage",
            "-s",
            help="Filter by stage name.",
        ),
    ] = None,
) -> None:
    """List items in the workshop.

    Shows all items with their current stage, or filter by stage.

    Examples:
        steward list
        steward list --stage forge
        steward list -s backlog
    """
    console = get_console()
    err_console = get_error_console()

    try:
        items = list_items(stage_filter)

        if not items:
            console.print("[dim]No items found[/dim]")
            raise typer.Exit(ExitCode.SUCCESS)

        console.print(f"[bold]Items ({len(items)}):[/bold]")
        for item in items:
            console.print(f"  {item.slug} [{item.stage.value}]")

        raise typer.Exit(ExitCode.SUCCESS)

    except ValueError:
        err_console.print(f"[red]Error:[/red] Invalid stage: {stage_filter}")
        valid_stages = ", ".join(s.value for s in Stage)
        err_console.print(f"[dim]Valid stages: {valid_stages}[/dim]")
        raise typer.Exit(ExitCode.INVALID_ARGUMENT) from None

    except WorkshopError as e:
        err_console.print(f"[red]Error:[/red] {e.message}")
        raise typer.Exit(ExitCode.ENV_ERROR) from None


if __name__ == "__main__":
    app()
