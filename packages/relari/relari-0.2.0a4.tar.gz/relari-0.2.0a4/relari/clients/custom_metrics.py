from typing import Dict, List, Union

from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod
from relari.metrics import MetricArgs, MetricDef
from dataclasses import dataclass
from relari.core.type_parser import str_to_type_hint


# @dataclass(frozen=True)
# class CustomMetric:
#     name: str
#     help: str
#     args: MetricArgs


class CustomMetricsClient:
    def __init__(self, client) -> None:
        self._client = client
        self._custom_metrics = self._get_custom_metrics()

    def _get_custom_metrics(self):
        response = self._client._request("metrics/custom/", HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get custom metrics", response=response)
        return [
            MetricDef(
                name=metric["name"],
                help=metric["help"],
                args=MetricArgs(
                    base={
                        kw: str_to_type_hint(val)
                        for kw, val in metric["args"]["base"].items()
                    },
                    ground_truth={
                        kw: str_to_type_hint(val)
                        for kw, val in metric["args"]["ground_truth"].items()
                    },
                ),
            )
            for metric in response.json()
        ]

    def list(self):
        return self._custom_metrics
    
    def __getitem__(self, name):
        for metric in self._custom_metrics:
            if metric.name == name:
                return metric
        raise KeyError(f"Custom metric '{name}' not found")