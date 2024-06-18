"""CLI module of dangling-finder"""

import time
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated

from dangling_finder.listing import _GraphQL
from dangling_finder.output import OutputFormat

err_console = Console(stderr=True)

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
)


def mutually_exclusive_group(size=1):
    group = []

    def callback(
        ctx: typer.Context, param: typer.CallbackParam, value: bool
    ):  # pylint: disable=unused-argument
        current_param = param.name.replace("_", "-")
        if value is True and current_param not in group:
            group.append(current_param)
        if len(group) > size:
            raise typer.BadParameter(
                f"{current_param} is mutually exclusive with {group[-2]}"
            )
        return value

    return callback


exclusivity_callback = mutually_exclusive_group()


@app.command("pull-requests", no_args_is_help=True)
def find_lost_pr_heads(
    owner: str,
    repo: str,
    github_token: Annotated[str, typer.Argument(envvar="GITHUB_TOKEN")],
    bash_script: Annotated[
        bool, typer.Option(callback=exclusivity_callback)
    ] = False,
    git_config: Annotated[
        bool, typer.Option(callback=exclusivity_callback)
    ] = False,
    batch: Annotated[int, typer.Option()] = 0,
):
    """List dangling commits SHA-1 in a GitHub repository's pull requests.
    NB: Only upper parents are returned.

    Args:
        owner (str): name of the repository owner
        repo (str): name of the repository
        github_token (str): personnal GitHub access token
        bash_script (bool): return bash script for local git repo
        git_config (bool): return a confgi config text to append
        batch (int): batch size of JSON output only.
    """
    graphql_api = _GraphQL(owner, repo, github_token)
    graphql_api.check_repository()
    pr_max = graphql_api.get_pull_request_highest_number()
    err_console.print(f"{pr_max} pull requests to scan.")
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=err_console,
    ) as progress:
        task1 = progress.add_task(
            description="Get all force-pushed events in PRs...", total=10
        )
        result1, old_rate_limit, prs = (
            graphql_api.execute_force_pushed_queries()
        )
        progress.update(
            task1, completed=10, description="Force-pushed PR events retrieved."
        )
        task2 = progress.add_task(
            description="Get all closed-and-not-merged PRs...", total=10
        )
        result2, rate_limit = graphql_api.execute_closed_pr_queries(
            prs, old_rate_limit
        )
        progress.update(
            task2,
            completed=10,
            description="Closed-and-not-merged PRs retrieved.",
        )
    duration = time.time() - start_time
    err_console.print(
        "Done. Duration: " + time.strftime("%H:%M:%S", time.gmtime(duration))
    )
    err_console.print("GitHub API quotas:")
    err_console.print(f'Remaining rate limit - {rate_limit["remaining"]}')
    err_console.print(f'Reset date rate limit - {rate_limit["resetAt"]}')
    err_console.print(f'Total cost used - {rate_limit["total"]}')
    output = OutputFormat(
        owner=owner,
        repo=repo,
        bash_script=bash_script,
        git_config=git_config,
        json_dangling_heads=result1 + result2,
        batch=batch
    ).output()
    typer.echo(output)


@app.command("events", no_args_is_help=True)
def find_latest_dangling_push_events():
    """WIP: find some danglign commits using latest push events
    """


if __name__ == "__main__":
    app()
