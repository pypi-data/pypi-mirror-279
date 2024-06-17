import json
from logging import getLogger
from typing import Any, Literal, TypedDict, cast

import yaml

from inspect_ai.util._context.subprocess import ExecResult, subprocess

from .config import auto_config
from .util import ComposeProject, tools_log

logger = getLogger(__name__)

# How long to wait for compose environment to pass a health check
COMPOSE_WAIT = "120"


async def compose_up(project: ComposeProject) -> None:
    # Start the environment
    result = await compose_command(
        ["up", "--detach", "--wait", "--wait-timeout", COMPOSE_WAIT],
        project=project,
    )
    if not result.success:
        msg = f"Failed to start docker services {result.stderr}"
        raise RuntimeError(msg)


async def compose_down(project: ComposeProject, quiet: bool = True) -> None:
    # shut down docker containers
    result = await compose_command(
        ["down", "--volumes"], project=project, capture_output=quiet, ansi="never"
    )
    if not result.success:
        msg = f"Failed to stop docker service {result.stderr}"
        logger.warning(msg)

    await compose_cleanup_images(project=project)


async def compose_cp(src: str, dest: str, project: ComposeProject) -> None:
    result = await compose_command(["cp", src, dest], project=project)
    if not result.success:
        msg = f"Failed to copy file from '{src}' to '{dest}'"
        raise RuntimeError(msg)


async def compose_check_running(services: list[str], project: ComposeProject) -> None:
    # Check to ensure that the status of containers is healthy
    running_services = await compose_ps("running", project=project)
    if len(running_services) > 0:
        if len(running_services) != len(services):
            unhealthy_services = services
            for running_service in running_services:
                unhealthy_services.remove(running_service["Service"])

            msg = f"One or more docker containers failed to start {','.join(unhealthy_services)}"
            raise RuntimeError(msg)
    else:
        raise RuntimeError("No services started")


async def compose_ps(
    status: Literal[
        "paused", "restarting", "removing", "running", "dead", "created", "exited"
    ],
    project: ComposeProject,
) -> list[dict[str, Any]]:
    result = await compose_command(
        ["ps", "--status", status, "--format", "json"],
        project=project,
    )
    if not result.success:
        msg = f"Error querying for running services: {result.stderr}"
        raise RuntimeError(msg)

    return [
        cast(dict[str, Any], json.loads(service))
        for service in result.stdout.strip().split("\n")
    ]


async def compose_build(project: ComposeProject, capture_output: bool = False) -> None:
    result = await compose_command(
        ["build"],
        project=project,
        capture_output=capture_output,
    )
    if not result.success:
        msg = "Failed to build docker containers"
        raise RuntimeError(msg)


async def compose_pull(
    service: str, project: ComposeProject, capture_output: bool = False
) -> ExecResult[str]:
    return await compose_command(
        ["pull", "--ignore-buildable", "--policy", "missing", service],
        project=project,
        capture_output=capture_output,
    )


async def compose_exec(
    command: list[str],
    project: ComposeProject,
    timeout: int | None = None,
    input: str | bytes | None = None,
) -> ExecResult[str]:
    return await compose_command(
        ["exec"] + command,
        project=project,
        timeout=timeout,
        input=input,
        forward_env=False,
    )


ComposeService = TypedDict(
    "ComposeService",
    {
        "image": str | None,
        "build": str | None,
        "x-default": bool | None,
        "x-local": bool | None,
    },
)


async def compose_services(project: ComposeProject) -> dict[str, ComposeService]:
    result = await compose_command(["config"], project=project)
    if not result.success:
        raise RuntimeError(f"Error reading docker config: {result.stderr}")
    return cast(dict[str, ComposeService], yaml.safe_load(result.stdout)["services"])


async def compose_cleanup_images(
    project: ComposeProject,
    timeout: int | None = None,
) -> None:
    tools_log("Removing images")
    # List the images that would be created for this compose
    images_result = await compose_command(["config", "--images"], project=project)

    # Remove those images explicitly
    if images_result.success:
        for image in images_result.stdout.strip().split("\n"):
            # See if this image was created by
            # inspect directly
            if image.startswith(project.name):
                # see if this image is present
                image_result = await subprocess(
                    ["docker", "images", "-q", image],
                    timeout=timeout,
                    capture_output=True,
                )

                remove_image = True
                if image_result.success:
                    remove_image = len(image_result.stdout) != 0

                # remove the image
                if remove_image:
                    result = await subprocess(
                        ["docker", "rmi", image],
                        timeout=timeout,
                        capture_output=True,
                    )
                    if not result.success:
                        msg = f"Failed to cleanup docker image {result.stderr}"
                        logger.warning(msg)


async def compose_command(
    command: list[str],
    project: ComposeProject,
    timeout: int | None = None,
    input: str | bytes | None = None,
    forward_env: bool = True,
    capture_output: bool = True,
    ansi: Literal["never", "always", "auto"] | None = None,
) -> ExecResult[str]:
    # The base docker compose command
    compose_command = ["docker", "compose"]

    # env to forward
    env = project.env if forward_env else {}

    # ansi
    if ansi:
        compose_command = compose_command + ["--ansi", ansi]

    # add project scope
    compose_command = compose_command + ["--project-name", project.name]

    # add config file if specified
    config = project.config if project.config else await auto_config()
    if config:
        compose_command = compose_command + ["-f", config]

    # build final command
    compose_command = compose_command + command

    # Execute the command
    tools_log(f"compose command: {compose_command}")
    result = await subprocess(
        compose_command,
        input=input,
        env=env,
        timeout=timeout,
        capture_output=capture_output,
    )
    tools_log(f"compose command (completed): {compose_command}")
    return result
