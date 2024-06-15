import requests
import uuid
import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict

from modulos_client import config as config_utils


class TestingLogBase(BaseModel):
    testing_metric_id: uuid.UUID
    value: str


class TestingLog(TestingLogBase):
    id: uuid.UUID
    created_at: datetime.datetime
    project_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


def log_metric(
    metric_id: str,
    value: str | int | float,
    project_id: str,
) -> TestingLog | None:
    client = config_utils.ModulosClient.from_conf_file()
    try:
        response = client.post(
            f"/v1/projects/{project_id}/testing/logs",
            data={
                "testing_metric_id": metric_id,
                "value": value,
            },
        )
    except requests.exceptions.ConnectionError:
        print("There was an issue with the connection. Please try again.")
        return None
    if response.status_code == 401:
        print("There was an issue with the authorization. Please login again.")

        return None
    if response.ok:
        print("Log successfully submitted.")
        return TestingLog.model_validate(response.json())
    else:
        print(f"Log submission failed: {response.text}")
        return None


class TestingMetricBase(BaseModel):
    name: str
    type: Literal["string", "integer", "float"]
    description: str


class TestingMetric(TestingMetricBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_by_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


def _get_modulos_client_source_id(project_id: str) -> str:
    """Get the source ID for the Modulos client."""
    # This is a easy fix

    client = config_utils.ModulosClient.from_conf_file()
    response = client.get(f"/v1/projects/{project_id}/testing/sources")
    if response.ok:
        sources = response.json()["items"]

        source = next((source for source in sources if source["mode"] == "push"), None)
        if source:
            return source["id"]
        else:
            raise ValueError("Could not find a push source for the project.")

    else:
        print(f"Could not get source ID: {response.text}")
        return ""


def create_metric(
    name: str,
    project_id: str,
    type: Literal["string", "integer", "float"],
    description: str,
) -> TestingMetric | None:
    client = config_utils.ModulosClient.from_conf_file()
    try:
        source_id = _get_modulos_client_source_id(project_id)
        response = client.post(
            f"/v1/projects/{project_id}/testing/sources/{source_id}/metrics",
            data={
                "name": name,
                "type": type,
                "description": description,
            },
        )
    except requests.exceptions.ConnectionError:
        print("There was an issue with the connection. Please try again.")
        return None
    if response.status_code == 401:
        print("There was an issue with the authorization. Please login again.")

        return None
    if response.ok:
        print("Metric successfully created.")
        return TestingMetric.model_validate(response.json())
    else:
        print(f"Metric creation failed: {response.text}")
        return None


def get_metrics(project_id: str) -> list[TestingMetric] | None:
    client = config_utils.ModulosClient.from_conf_file()
    try:
        source_id = _get_modulos_client_source_id(project_id)
        response = client.get(
            f"/v1/projects/{project_id}/testing/sources/{source_id}/metrics"
        )
    except requests.exceptions.ConnectionError:
        print("There was an issue with the connection. Please try again.")
        return None
    if response.status_code == 401:
        print("There was an issue with the authorization. Please login again.")
        return None
    if response.ok:
        return [
            TestingMetric.model_validate(metric) for metric in response.json()["items"]
        ]
    else:
        print(f"Could not get metrics: {response.text}")
        return None


def get_metric(metric_id: str, project_id: str) -> TestingMetric | None:
    client = config_utils.ModulosClient.from_conf_file()
    try:
        source_id = _get_modulos_client_source_id(project_id)
        response = client.get(
            f"/v1/projects/{project_id}/testing/sources/{source_id}/metrics/{metric_id}"
        )
    except requests.exceptions.ConnectionError:
        print("There was an issue with the connection. Please try again.")
        return None
    if response.status_code == 401:
        print("There was an issue with the authorization. Please login again.")
        return None
    if response.ok:
        return TestingMetric.model_validate(response.json())
    else:
        print(f"Could not get metric: {response.text}")
        return None
