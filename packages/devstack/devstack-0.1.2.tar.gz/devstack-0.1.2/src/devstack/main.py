#!/usr/bin/env python3
"""A tool for managing docker swarm stacks."""

import logging
import os
import shlex
import subprocess
from pathlib import Path
from typing import Annotated

import typer
import yaml

try:
    logging.basicConfig(level=logging.getLevelName(os.environ.get("DS_LOG_LEVEL", "WARNING")))
except ValueError:
    logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("devstack")

app = typer.Typer(no_args_is_help=True)


def _complete_files(incomplete: str) -> str:
    for e in Path().glob(pattern=f"{incomplete}*"):
        if e.is_file() and e.suffix in {".yml", ".yaml"}:
            logger.debug("incomplete %s, yield %s", incomplete, e.name)
            yield e.name


def _complete_services(ctx: typer.Context, incomplete: str) -> str:
    stack_file = ctx.params.get("stack_file")
    with Path(stack_file).open() as compose:
        data = yaml.safe_load(compose)
        services = data.get("services", {})
        for service in services:
            if service.startswith(incomplete):
                yield service


StackFile = Annotated[
    Path,
    typer.Argument(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        autocompletion=_complete_files,
    ),
]

Service = Annotated[
    str,
    typer.Argument(autocompletion=_complete_services),
]


def _get_external_network_list(stack_file: Path) -> list[str]:
    networks: list[str] = []
    with stack_file.open() as compose:
        data = yaml.safe_load(compose)
        for k, v in data["networks"].items():
            if not v["external"]:
                continue
            networks.append(v.get("name", k))
    return networks


def _create_networks(stack_file: Path) -> None:
    networks = _get_external_network_list(stack_file)
    for network in networks:
        cmd = shlex.split(f"docker network create --driver overlay --attachable {network}")
        subprocess.run(cmd, check=False)


@app.command("create")
def _create(
    *,
    stack_file: StackFile,
) -> None:
    _create_networks(stack_file)
    cmd = shlex.split(f"docker stack deploy --compose-file {stack_file} --prune {stack_file.stem}")
    subprocess.run(cmd, check=False)


@app.command("destroy")
def _destroy(
    *,
    stack_file: StackFile,
) -> None:
    cmd = shlex.split(f"docker stack rm {stack_file.stem}")
    subprocess.run(cmd, check=False)


@app.command("status")
def _status(
    *,
    stack_file: StackFile,
) -> None:
    cmd = shlex.split(f"docker stack services {stack_file.stem}")
    subprocess.run(cmd, check=False)


@app.command("logs")
def _logs(
    *,
    stack_file: StackFile,
    service: Service,
    follow: bool = True,
) -> None:
    cmd = shlex.split(f"docker service logs {'-f' if follow else ''} {stack_file.stem}_{service}")
    subprocess.run(cmd, check=False)


def _get_container_id(stack_name: str, service: str) -> str | None:
    query = f"{stack_name}_{service}"
    cmd = shlex.split('docker container ls --format "{{.ID}} {{.Names}}"')
    res = subprocess.run(cmd, check=False, capture_output=True)
    for raw_line in res.stdout.splitlines():
        line = raw_line.decode()
        if query in line:
            logger.debug("_get_container_id: query: %s line: %s", query, line)
            return line.split(" ")[0]
    logger.debug("_get_container_id: query: %s, container not found", query)
    return None


@app.command("exec")
def _exec(
    *,
    stack_file: StackFile,
    service: Service,
    command: str,
) -> None:
    stack_name = stack_file.stem
    container_id = _get_container_id(stack_name, service)
    if container_id is None:
        typer.echo(f"Service {service} not found in stack {stack_name}")
        raise typer.Exit(1)
    cmd = shlex.split(f"docker exec -it {container_id} {command}")
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    app()
