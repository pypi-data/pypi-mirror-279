import logging

import beaupy
import rich
import typer

from launchflow import exceptions
from launchflow.cli.constants import ENVIRONMENT_HELP
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.config import config
from launchflow.flows.environments_flows import get_environment
from launchflow.managers.project_manager import ProjectManager

app = UTyper(help="Commands for viewing services managed by LaunchFlow")


@app.command()
async def list(environment: str = typer.Argument(..., help=ENVIRONMENT_HELP)):
    """List all services in a project/environment."""
    ps_manager = ProjectManager(
        backend=config.launchflow_yaml.backend, project_name=config.project
    )
    environment_name, env = await get_environment(
        ps_manager,
        environment_name=environment,
        prompt_for_creation=False,
    )
    environment_manager = ps_manager.create_environment_manager(environment_name)
    services = await environment_manager.list_services()
    print_response(
        "Services",
        {
            name: service.model_dump(
                mode="json", exclude_defaults=True, exclude_none=True
            )
            for name, service in services.items()
        },
    )


@app.command()
async def unlock(
    environment: str = typer.Argument(..., help=ENVIRONMENT_HELP),
    service: str = typer.Argument(..., help="The service to unlock."),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve environment force unlock."
    ),
):
    """Force unlock a service."""
    ps_manager = ProjectManager(
        backend=config.launchflow_yaml.backend, project_name=config.project
    )
    environment_name, env = await get_environment(
        ps_manager,
        environment_name=environment,
        prompt_for_creation=False,
    )
    environment_manager = ps_manager.create_environment_manager(environment_name)
    service_manager = environment_manager.create_service_manager(service)
    try:
        await service_manager.load_service()
    except exceptions.ServiceNotFound:
        rich.print(
            f"[red]Service '{service}' not found in Environment '{environment_name}'.[/red]"
        )
        raise typer.Exit(1)

    if not auto_approve:
        rich.print(
            f"[yellow]Are you sure you want to force unlock Service '{service}'? This can lead to data corruption or conflicts.[/yellow]"
        )
        # TODO: Link to docs that explain what force unlock does
        if not beaupy.confirm("Force unlock Service?"):
            rich.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(0)

    try:
        await service_manager.force_unlock_service()
        rich.print(
            f"[green]Service '{service}' force unlocked in Environment '{environment_name}'.[/green]"
        )
    except exceptions.EntityNotLocked:
        rich.print(
            f"[yellow]Service '{service}' is not locked. Nothing to unlock.[/yellow]"
        )
        raise typer.Exit(1)
    except Exception as e:
        logging.exception("Exception occurred: %s", e)
        logging.debug("Exception occurred: %s", e, exc_info=True)
        rich.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
