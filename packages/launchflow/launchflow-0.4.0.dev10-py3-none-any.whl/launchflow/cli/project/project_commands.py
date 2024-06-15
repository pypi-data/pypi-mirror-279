import os
from typing import Optional

import beaupy
import httpx
import rich
import typer

from launchflow import exceptions
from launchflow.backend import LaunchFlowBackend, LocalBackend
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.clients import async_launchflow_client_ctx
from launchflow.clients.projects_client import ProjectsAsyncClient
from launchflow.config import config
from launchflow.exceptions import LaunchFlowException
from launchflow.flows.project_flows import create_project
from launchflow.validation import validate_project_name

app = UTyper(help="Interact with your LaunchFlow projects.")


@app.command()
async def list():
    """Lists all current projects in your account."""
    try:
        backend = config.launchflow_yaml.backend
    except exceptions.LaunchFlowYamlNotFound:
        typer.echo("launchflow.yaml was not found. Please run `lf init` to create one.")
        raise typer.Exit(1)

    if isinstance(backend, LocalBackend):
        if not os.path.exists(backend.path):
            typer.echo("No local projects found.")
            raise typer.Exit(0)
        local_project_folders = os.listdir(backend.path)
        if not local_project_folders:
            typer.echo("No local projects found.")
            raise typer.Exit(0)
        print_response(
            "Projects",
            {
                "projects (local)": [
                    {"name": project, "path": os.path.join(backend.path, project)}
                    for project in local_project_folders
                ]
            },
        )
        return

    if not isinstance(backend, LaunchFlowBackend):
        typer.echo(
            f"Unsupported backend: {type(backend)}. This command only supports local and LaunchFlow Cloud backends."
        )
        raise typer.Exit(1)

    base_url = config.get_launchflow_cloud_url()
    account_id = config.get_account_id()
    async with httpx.AsyncClient(timeout=60) as client:
        proj_client = ProjectsAsyncClient(
            http_client=client, launchflow_account_id=account_id, base_url=base_url
        )
        projects = await proj_client.list()
    print_response(
        "Projects",
        {
            "projects": [
                projects.model_dump(exclude_defaults=True) for projects in projects
            ]
        },
    )


@app.command()
async def create(
    project: Optional[str] = typer.Argument(None, help="The project name."),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve project creation."
    ),
):
    """Create a new project in your account."""
    if not isinstance(config.launchflow_yaml.backend, LaunchFlowBackend):
        typer.echo(
            "This command only supports LaunchFlow Cloud backends. Please run `lf init --backend=lf` to create a LaunchFlow Cloud backend."
        )
        raise typer.Exit(1)
    # TODO: Make this a separate utility and update other CRUD commands to use it
    if project is None:
        if auto_approve:
            typer.echo(
                "Project name is required for auto approval. (i.e. `lf projects create my-project -y`)"
            )
            raise typer.Exit(1)
        project = beaupy.prompt("What would you like to name your LaunchFlow project?")
        while True:
            valid, reason = validate_project_name(project, raise_on_error=False)
            if valid:
                break
            else:
                rich.print(f"[red]{reason}[/red]")
                project = beaupy.prompt("Please enter a new project name.")
    else:
        validate_project_name(project)

    async with httpx.AsyncClient(timeout=60) as client:
        proj_client = ProjectsAsyncClient(
            http_client=client,
            launchflow_account_id=config.get_account_id(),
            base_url=config.get_launchflow_cloud_url(),
        )
        try:
            project = await create_project(
                client=proj_client,
                project_name=project,
                account_id=config.get_account_id(),
                prompt=not auto_approve,
            )
        except LaunchFlowException:
            raise typer.Exit(1)

    if project is not None:
        print_response("Project", project.model_dump(exclude_defaults=True))


@app.command()
async def delete(
    name: str = typer.Argument(..., help="The project name."),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve project deletion."
    ),
):
    """Delete a project."""
    base_url = config.get_launchflow_cloud_url()

    async with async_launchflow_client_ctx(
        config.get_account_id(),
        base_url=base_url,
    ) as client:
        try:
            await client.projects.get(name)
        except exceptions.ProjectNotFound:
            rich.print(f"[red]Project '{name}' not found.[/red]")
            raise typer.Exit(1)

        if not auto_approve:
            user_confirmation = beaupy.confirm(
                f"Would you like to delete the project `{name}`?",
                default_is_yes=True,
            )
            if not user_confirmation:
                rich.print("[red]✗[/red] Project deletion cancelled.")
                typer.Exit(1)

        try:
            await client.projects.delete(name)
            rich.print("[green]✓[/green] Project deleted.")
        except Exception as e:
            typer.echo(e)
            raise typer.Exit(1)
