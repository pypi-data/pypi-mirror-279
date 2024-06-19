import datetime
import json
import re
from pathlib import Path

import click
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from relari.core.utils import from_timestamp

from relari import Dataset, RelariClient

ID_COL_WIDTH = 24

client = RelariClient()
console = Console()


def _usage_color(percentage):
    return next(
        (color for limit, color in [(90, "red"), (50, "yellow")] if percentage > limit),
        "green",
    )


def convert_to_lowercase_filename(name):
    cleaned_name = re.sub(r"[^a-zA-Z0-9\s-]", "", name)
    underscored_name = cleaned_name.replace(" ", "_").replace("-", "_")
    lowercase_filename = underscored_name.lower()
    return lowercase_filename


@click.group()
def cli():
    pass


@cli.group()
def projects():
    """Commands related to projects"""
    pass


@projects.command("ls")
def list_projects():
    """List all projects"""
    projects = client.projects.list()
    table = Table(show_header=True, header_style="bold")
    table.add_column("Project ID", style="dim", width=ID_COL_WIDTH)
    table.add_column("Name")
    for proj in projects:
        table.add_row(proj["id"], proj["name"])
    console.print(table)


@projects.command("new")
@click.argument("project_name")
def new_project(project_name):
    """Create a new project"""
    click.echo(f"Creating new project: `{project_name}`")
    proj = client.projects.create(project_name)
    rprint(f"Project created: {proj['id']}")


@cli.group()
def datasets():
    """Commands related to datasets"""
    pass


@datasets.command("ls")
@click.argument("project_id")
def list_datasets(project_id):
    """List all datasets in a project"""
    click.echo(f"Listing all datasets in project: {project_id}")
    try:
        datasets = client.datasets.list(project_id)
        table = Table(show_header=True, header_style="bold")
        table.add_column("Dataset ID", style="dim", width=ID_COL_WIDTH)
        table.add_column("Name")
        table.add_column("Description", width=50, overflow="fold")
        table.add_column("Size")
        table.add_column("License")
        table.add_column("Fields")
        for dataset in datasets:
            table.add_row(
                dataset["id"],
                dataset["name"],
                dataset["manifest"]["description"],
                str(dataset["size"]),
                dataset["manifest"]["license"],
                "\n".join(dataset["manifest"]["fields"]),
            )
        console.print(table)
    except ValueError as e:
        rprint(f"[bold red] {e}[/bold red]")


@datasets.command("new")
@click.argument("project_id")
@click.argument("path", type=click.Path(exists=True))
def new_dataset(project_id, path):
    """Create a new dataset in a project"""
    click.echo(f"Uploading {path} to project {project_id}")
    res = client.datasets.create(project_id=project_id, dataset=Dataset(path))
    rprint(f"Dataset created: {res['id']}")


@datasets.command("get")
@click.argument("dataset_name")
@click.argument(
    "out_dir",
    type=click.Path(exists=False, writable=True, dir_okay=True, file_okay=False),
)
def get_dataset(dataset_name, out_dir):
    """Get a dataset from a project"""
    click.echo(f"Getting dataset {dataset_name} ")
    out_dir = Path(out_dir)
    try:
        if (out_dir / "dataset.json").exists():
            rprint(f"[bold red]Dataset already exists at {out_dir}[/bold red]")
            return
        if (out_dir / "manifest.yaml").exists():
            rprint(f"[bold red]Manifest already exists at {out_dir}[/bold red]")
            return
        dataset = client.datasets.get(dataset_name)
        dataset.save(out_dir / "dataset.json", save_manifest=True)
    except ValueError as e:
        rprint(f"[bold red]{e}[/bold red]")


@cli.group()
def evaluations():
    """Commands related to evaluations"""
    pass


@evaluations.command("ls")
@click.argument("project_id")
@click.option("--show-metadata", is_flag=True, default=False, help="Show metadata")
def list_evaluations(project_id, show_metadata):
    """List all evaluations in a project"""
    click.echo(f"Listing all evaluations in project: {project_id}")
    try:
        evaluations = client.evaluations.list(project_id)
        table = Table(show_header=True, header_style="bold")
        table.add_column("Evaluation ID", style="dim", width=ID_COL_WIDTH)
        table.add_column("Dataset ID", style="dim", width=ID_COL_WIDTH)
        table.add_column("Name")
        table.add_column("Timestamp")
        if show_metadata:
            table.add_column("Metadata")
        table.add_column("Status")
        for evl in evaluations:
            row_data = [
                evl["id"],
                evl["dataset"],
                evl["name"],
                datetime.datetime.fromtimestamp(evl["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                evl["status"],
            ]
            if show_metadata:
                row_data.insert(4, json.dumps(evl["metadata"], indent=2))
            table.add_row(*row_data)
        console.print(table)
    except ValueError as e:
        rprint(f"[bold red] {e}[/bold red]")


@evaluations.command("status")
@click.argument("evaluation_id")
def status_evaluations(evaluation_id):
    """Retrieve the status of an evaluation"""
    try:
        evaluations = client.evaluations.get(evaluation_id)
        print(evaluations["status"])
    except ValueError as e:
        rprint(f"[bold red] {e}[/bold red]")


@evaluations.command("get")
@click.argument("evaluation_id")
def get_evaluation(evaluation_id):
    """Get an evaluation from a project"""
    click.echo(f"Getting evaluation {evaluation_id}")
    try:
        eval_data = client.evaluations.get(evaluation_id)
        with open(f"{convert_to_lowercase_filename(eval_data['name'])}.json", "w") as f:
            json.dump(eval_data, f, indent=2)
        rprint(
            f"Saved evaluation to {convert_to_lowercase_filename(eval_data['name'])}.json"
        )
    except ValueError as e:
        rprint(f"[bold red]{e}[/bold red]")


@cli.group()
def metrics():
    """Commands related to metrics"""
    pass


@metrics.command("ls")
@click.option(
    "--custom-only", is_flag=True, default=False, help="Show only custom metrics"
)
def list_metrics(custom_only):
    """List all metrics"""

    def _add_to_table(table, metric):
        table.add_row(
            metric.name,
            metric.help,
            "\n".join([f"{k}: {v}" for k, v in metric.args.base.items()]),
            "\n".join([f"{k}: {v}" for k, v in metric.args.ground_truth.items()]),
        )

    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Input")
    table.add_column("Ground Truth (Optional)")
    if not custom_only:
        for metric in client.metrics.list():
            _add_to_table(table, metric)
    for metric in client.custom_metrics.list():
        _add_to_table(table, metric)
    console.print(table)


@cli.group()
def usage():
    """Commands related to usage"""
    pass


@usage.command("info")
def usage_info():
    """Get current usage information"""
    info = client.usage.get_current()
    percentage = info["used"] / info["limit"] * 100
    c = _usage_color(percentage)
    rprint(
        f"[bold]Usage:[/bold] [{c}]{info['used']} / {info['limit']} ({percentage:.2f}%)[/{c}]"
    )


@usage.command("history")
def usage_history():
    """Get usage history"""
    history = client.usage.get_history()
    table = Table(show_header=True, header_style="bold")
    table.add_column("Start Date")
    table.add_column("End Date")
    table.add_column("Used")
    table.add_column("Limit")
    for entry in history:
        percentage = entry["usage"] / entry["limit"] * 100
        start = from_timestamp(entry["start_date"]).strftime("%Y-%m-%d")
        end = from_timestamp(entry["end_date"]).strftime("%Y-%m-%d")
        table.add_row(
            start,
            end,
            str(entry["usage"]),
            str(entry["limit"]),
            style=_usage_color(percentage),
        )
    console.print(table)


if __name__ == "__main__":
    cli()
