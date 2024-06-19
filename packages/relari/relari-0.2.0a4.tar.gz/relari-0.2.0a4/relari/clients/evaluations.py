import json
from typing import Any, Dict, List, Optional

from relari.core.exceptions import APIError
from relari.core.types import HTTPMethod
from relari.metrics import Metric
from relari.core.types import DatasetDatum


class EvaluationsClient:
    def __init__(self, client):
        self._client = client

    def list(self, project_id: str):
        endpoint = f"projects/{project_id}/experiments/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to list evaluations", response=response)
        return response.json()

    def get(self, experiment_id: str):
        endpoint = f"projects/experiments/{experiment_id}/"
        response = self._client._request(endpoint, HTTPMethod.GET)
        if response.status_code != 200:
            raise APIError(message="Failed to get evaluation", response=response)
        return response.json()
    
    def find(self, name: str):
        lst = self.list()
        out = list()
        name_ = name.strip()
        for d in lst:
            if d["name"].strip() == name_:
                out.append(d)
        if len(out) == 0:
            return None
        if len(out) == 1:
            return out[0]
        return out

    def submit(
        self,
        project_id: str,
        name: Optional[str],
        pipeline: List[Metric],
        data: List[Dict[str, Any]],
        dataset: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = dict(),
    ):
        if not all(isinstance(m, Metric) for m in pipeline):
            raise ValueError("pipeline must be a list of Metric")
        if dataset is not None:
            if not all(isinstance(d, DatasetDatum) for d in data):
                raise ValueError(
                    "data must be a list of DatasetDatum if dataset is provided"
                )
            for metric in pipeline:
                [metric.args.validate(x.data, with_optional=False) for x in data]
            data_ = [x.asdict() for x in data]
        else:
            for metric in pipeline:
                [metric.args.validate(x, with_optional=True) for x in data]
            data_ = data
        endpoint = f"projects/{project_id}/experiments/"
        payload = {
            "name": name,
            "pipeline": [metric.value for metric in pipeline],
            "data": data_,
            "dataset": dataset,
            "metadata": metadata,
        }
        res = self._client._request(endpoint, HTTPMethod.POST, data=json.dumps(payload))
        if res.status_code != 200:
            raise APIError(message="Failed to submit evaluation", response=res)
        return res.json()
