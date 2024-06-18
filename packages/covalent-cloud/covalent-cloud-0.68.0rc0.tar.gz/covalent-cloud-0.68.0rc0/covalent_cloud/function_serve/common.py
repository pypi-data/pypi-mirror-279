# Copyright 2024 Agnostiq Inc.

import time
from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from covalent_cloud.function_serve.models import Deployment

__all__ = [
    "DEPLOY_ELECTRON_PREFIX",
    "SupportedMethods",
    "ServiceStatus",
    "rename",
    "wait_for_deployment_to_be_active",
]


DEPLOY_ELECTRON_PREFIX = "#__deploy_electron__#"

# 120 retries * 30 seconds = 60 minutes
ACTIVE_DEPLOYMENT_RETRIES = 120
ACTIVE_DEPLOYMENT_POLL_INTERVAL = 30


class SupportedMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ServiceStatus(str, Enum):
    """Possible statuses for a function service."""

    NEW_OBJECT = "NEW_OBJECT"
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"


class ServeAssetType(str, Enum):
    """Possible types for the ServeAsset `type` field."""

    ASSET = "Asset"
    JSON = "JSON"


def rename(name):
    def decorator(fn):
        fn.__name__ = name
        return fn

    return decorator


def wait_for_deployment_to_be_active(
    deployment: "Deployment", verbose=False
) -> "Deployment":
    """Repeatedly reload the deployment and handle status updates."""
    retries_done = 0
    while (
        retries_done < ACTIVE_DEPLOYMENT_RETRIES
        and deployment.status not in [
            ServiceStatus.ERROR,
            ServiceStatus.ACTIVE,
            ServiceStatus.INACTIVE,
        ]
    ):
        if verbose:
            print("Deployment info is: ")
            print(deployment)

        time.sleep(ACTIVE_DEPLOYMENT_POLL_INTERVAL)

        deployment.reload()
        retries_done += 1

    if deployment.status in [
        ServiceStatus.ACTIVE,
        ServiceStatus.ERROR,
    ]:
        return deployment

    if deployment.status == ServiceStatus.INACTIVE:

        # Reload one last time to get any error message
        deployment.reload()
        if deployment.error:
            return deployment

        # If the deployment is inactive and there is no error message, raise an error
        raise RuntimeError("Deployment is inactive")

    raise RuntimeError(
        f"Timed out after {ACTIVE_DEPLOYMENT_RETRIES * ACTIVE_DEPLOYMENT_POLL_INTERVAL / 60} "
        "minutes while waiting for the deployment to become active"
    )
