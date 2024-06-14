import json
from typing import Optional, List, Any, Dict

from pydantic import BaseModel, PrivateAttr, TypeAdapter, computed_field, Field, FilePath

from ipfabric.tools import raise_for_status

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

OAS_DIR = files("ipfabric.oas")


class Endpoint(BaseModel):
    api_endpoint: str
    method: str
    web_endpoint: Optional[str] = None
    columns: Optional[List[str]] = None
    nested_columns: Optional[List[str]] = None
    ui_columns: Optional[List[str]] = None
    api_scope_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None

    def __repr__(self):
        return f"({self.method}, {self.api_endpoint})"


class Methods(BaseModel):
    api_endpoint: str
    get: Optional[Endpoint] = None
    put: Optional[Endpoint] = None
    patch: Optional[Endpoint] = None
    post: Optional[Endpoint] = None
    delete: Optional[Endpoint] = None


class OAS(BaseModel):
    client: Any = Field(exclude=True)
    local_oas: bool = True
    local_oas_file: Optional[FilePath] = None
    _oas: Dict[str, Methods] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context) -> None:
        self._oas = self._get_oas()

    @property
    def oas(self) -> Dict[str, Methods]:
        return self._oas

    def _get_oas(self) -> Dict[str, Methods]:
        if not self.local_oas or (self.local_oas_file and self.local_oas):
            return self._parse_oas()
        try:
            min_oas = OAS_DIR.joinpath(self.client.api_version + ".json").read_text()
            oas = TypeAdapter(Dict[str, Methods]).validate_json(min_oas)
            return oas
        except FileNotFoundError:
            return self._parse_oas()

    @computed_field
    @property
    def web_to_api(self) -> Dict[str, Endpoint]:
        return {m.post.web_endpoint: m.post for m in self._oas.values() if m.post and m.post.web_endpoint}

    @computed_field
    @property
    def scope_to_api(self) -> Dict[str, Endpoint]:
        _ = dict()
        for methods in self._oas.values():
            for method in ["get", "put", "post", "patch", "delete"]:
                m = getattr(methods, method, None)
                if m and m.api_scope_id:
                    _[m.api_scope_id] = m
        return _

    @staticmethod
    def _post_logic(data: Endpoint, spec: dict):
        try:
            data.web_endpoint = spec["x-table"]["webPath"]
        except KeyError:
            pass
        try:
            data.ui_columns = [_["key"] for _ in spec["x-table"]["columns"]]
        except KeyError:
            pass
        try:
            columns = set(
                spec["requestBody"]["content"]["application/json"]["schema"]["properties"]["columns"]["items"]["enum"]
            )
            data.columns = list(columns)
        except KeyError:
            pass
        try:
            columns = spec["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["data"]["items"][
                "properties"
            ]
            data.nested_columns = [k for k, v in columns.items() if "type" in v and v["type"] == "array"]
        except KeyError:
            pass
        return data

    def _parse_oas(self) -> Dict[str, Methods]:
        if not self.local_oas:
            oas = raise_for_status(
                self.client.get(self.client.base_url.join("/api/oas/openapi-extended.json"), follow_redirects=True)
            ).json()
        else:
            with open(self.local_oas_file, 'r') as f:
                oas = json.load(f)

        endpoints = dict()
        for endpoint, methods in oas["paths"].items():
            methods_obj = Methods(api_endpoint=endpoint)
            for method, spec in methods.items():
                data = Endpoint(
                    api_endpoint=endpoint[1:],
                    method=method,
                    api_scope_id=spec.get("x-apiScopeId", None),
                    summary=spec.get("summary", None),
                    description=spec.get("description", None),
                )
                if method == "post":
                    data = self._post_logic(data, spec)
                setattr(methods_obj, method, data)
            endpoints[endpoint[1:]] = methods_obj
        return endpoints
