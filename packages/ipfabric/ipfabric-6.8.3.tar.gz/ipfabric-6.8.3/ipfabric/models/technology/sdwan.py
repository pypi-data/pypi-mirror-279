import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Sdwan(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    @computed_field
    @property
    def sites(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/sites", sn=self.sn)

    @computed_field
    @property
    def links(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/links", sn=self.sn)
